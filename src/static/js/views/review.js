import { startEventStream, showToast } from '../utils.js';
import { loadDashboardData } from './dashboard.js';

export let lastReviewedFile = "";

export function runReviewPipeline() {
    const selectEl = document.getElementById('review-file-select');
    if (!selectEl) return;
    const fileName = selectEl.value;
    if (!fileName) {
        alert('ファイルを選択してください');
        return;
    }

    // 表示をコンソールログ表示モードに切り替える
    const header = document.getElementById('review-preview-header');
    const consoleHeader = document.getElementById('review-console-header');
    const previewBody = document.getElementById('review-preview-body');
    const consoleLog = document.getElementById('review-console-log');
    
    if (header) header.style.display = 'none';
    if (consoleHeader) consoleHeader.style.display = 'flex';
    if (previewBody) previewBody.style.display = 'none';
    if (consoleLog) consoleLog.style.display = 'block';

    const btn = document.getElementById('btn-run-review');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '🔍 レビュー実行中...';
    }

    lastReviewedFile = fileName;

    const modelVal = document.getElementById('review-model').value;
    let url = `/api/stream/review?file=${encodeURIComponent(fileName)}`;
    if (modelVal) {
        url += `&model=${encodeURIComponent(modelVal)}`;
    }
    startEventStream(url, 'review-console-log', 'review-console-status', (success) => {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '🔍 レビューパイプラインを実行';
        }
        if (success) {
            showToast('レビューパイプラインが正常に完了しました');
            loadDashboardData();
        } else {
            showToast('レビュー中にエラーが発生しました');
        }
    });
}
