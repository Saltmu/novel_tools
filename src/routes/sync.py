import datetime
import os
from pathlib import Path

from fastapi import APIRouter

from src.services import novel_service
from src.utils import project_config as writer_helper
from src.utils import project_paths
from src.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/api/stream/sync")
async def stream_sync():
    cmd = ["poetry", "run", "python", "-u", "src/sync_gdrive.py"]
    return novel_service.stream_process_output(cmd)


@router.get("/api/sync/status")
async def sync_status():
    sources_dir = Path(project_paths.get_sources_dir())
    if not sources_dir.exists():
        return {"sources": []}

    sources_list = []
    for f in sorted(sources_dir.glob("*.txt"), key=writer_helper.natural_sort_key):
        mtime = os.path.getmtime(f)
        dt = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        sources_list.append(
            {"name": f.name, "size": f.stat().st_size, "last_updated": dt}
        )
    return {"sources": sources_list}
