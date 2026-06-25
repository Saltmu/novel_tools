import { startEventStream, showToast } from '../utils.js';
import { loadDashboardData } from './dashboard.js';

export function runDriveSync() {
    const btn = document.getElementById('btn-run-sync');
    if (btn) btn.disabled = true;

    startEventStream('/api/stream/sync', 'sync-console-log', 'sync-console-status', (success) => {
        if (btn) btn.disabled = false;
        if (success) {
            showToast('同期が正常に完了しました');
            loadDashboardData();
        } else {
            showToast('同期中にエラーが発生しました');
        }
    });
}
