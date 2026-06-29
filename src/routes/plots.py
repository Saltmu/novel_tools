import datetime
import os
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query

from src.services import novel_service
from src.utils import project_config as writer_helper
from src.utils import project_paths
from src.utils.logger import get_logger
from src.utils.yaml_handler import YamlHandler

router = APIRouter()
logger = get_logger(__name__)


@router.get("/api/plots")
async def list_plots():
    sources_dir = Path(project_paths.get_sources_dir())
    if not sources_dir.exists():
        return {"plots": []}

    plots_list = []
    for f in sorted(sources_dir.glob("*.txt"), key=writer_helper.natural_sort_key):
        name = f.name
        if "プロット" in name or "plot" in name.lower() or name == "第1幕概要.txt":
            plot_stem = f.stem
            yaml_path = project_paths.get_plot_findings_yaml_path(
                project_paths.get_output_dir(plot_stem), plot_stem
            )
            has_findings = os.path.exists(yaml_path)

            mtime = os.path.getmtime(f)
            dt = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")

            plots_list.append(
                {
                    "name": name,
                    "size": f.stat().st_size,
                    "mtime": dt,
                    "has_findings": has_findings,
                }
            )
    return {"plots": plots_list}


@router.get("/api/plot")
async def get_plot(
    file: str = Query(
        ..., description=f"Plot filename in {project_paths.DATA_SOURCES_DIR}/"
    ),
):
    safe_file = os.path.basename(file)
    plot_path = project_paths.get_source_path(safe_file)
    if not os.path.exists(plot_path):
        raise HTTPException(status_code=404, detail="Plot file not found.")

    with open(plot_path, encoding="utf-8") as f:
        content = f.read()

    plot_stem = Path(plot_path).stem
    yaml_path = project_paths.get_plot_findings_yaml_path(
        project_paths.get_output_dir(plot_stem), plot_stem
    )
    findings = []
    if os.path.exists(yaml_path):
        try:
            data = YamlHandler.load_safe(yaml_path)
            if data and "findings" in data:
                findings = data["findings"]
        except Exception as e:
            logger.error(f"Error reading plot YAML findings: {e}", exc_info=True)

    return {
        "plot_name": safe_file,
        "content": content,
        "findings": findings,
    }


@router.get("/api/stream/plot_review")
async def stream_plot_review(
    file: str = Query(
        ..., description=f"Plot filename in {project_paths.DATA_SOURCES_DIR}/"
    ),
    model: str | None = Query(None),
):
    safe_file = os.path.basename(file)
    plot_path = project_paths.get_source_path(safe_file)
    if not os.path.exists(plot_path):
        raise HTTPException(status_code=404, detail="Plot file not found.")

    cmd = [
        "poetry",
        "run",
        "python",
        "-u",
        "src/run_plot_review_pipeline.py",
        plot_path,
    ]
    if model:
        cmd.extend(["--model", model])

    return novel_service.stream_process_output(cmd)
