import { state } from './state.js';

export function parseLineNumber(locationStr) {
    if (!locationStr) return null;
    const match = String(locationStr).match(/(\d+)/);
    return match ? parseInt(match[0], 10) : null;
}

export function showToast(message, duration = 1500) {
    const toast = document.getElementById('toast');
    if (toast) {
        toast.textContent = message;
        toast.classList.add('show');
        setTimeout(() => { toast.classList.remove('show'); }, duration);
    }
}

export function showModal(id) { 
    const el = document.getElementById(id);
    if (el) el.classList.add('active'); 
}

export function closeModal(id) { 
    const el = document.getElementById(id);
    if (el) el.classList.remove('active'); 
}

export function startEventStream(url, consoleId, statusId, onComplete = null) {
    const consoleEl = document.getElementById(consoleId);
    const statusEl = document.getElementById(statusId);
    if (!consoleEl || !statusEl) return;
    
    consoleEl.textContent = '--- プロセスを開始します ---\n';
    statusEl.textContent = 'RUNNING';
    statusEl.style.color = '#fbbf24'; // Amber

    // 自動的に右側コンソールパネルを開く
    const rightPanel = consoleEl.closest('.right-panel');
    if (rightPanel) {
        rightPanel.classList.add('show');
        const viewEl = consoleEl.closest('.view-content');
        if (viewEl) {
            updateToggleButtonText(viewEl.id, true);
        }
    }

    document.body.classList.add('process-running');
    state.isRunningProcess = true;

    const eventSource = new EventSource(url);

    eventSource.onmessage = function(event) {
        if (event.data.includes('[PROCESS_EXITED]')) {
            const code = event.data.split('code=')[1] || '0';
            consoleEl.textContent += `\n--- プロセスが終了しました (終了コード: ${code}) ---\n`;
            statusEl.textContent = code === '0' ? 'COMPLETED' : 'FAILED';
            statusEl.style.color = code === '0' ? '#34d399' : '#f87171';
            eventSource.close();
            
            document.body.classList.remove('process-running');
            state.isRunningProcess = false;

            if (onComplete) onComplete(code === '0');
            return;
        }
        consoleEl.textContent += event.data + '\n';
        consoleEl.scrollTop = consoleEl.scrollHeight; // Auto scroll
    };

    eventSource.onerror = function(err) {
        consoleEl.textContent += '\n[ERROR] 接続エラーまたはサーバーが切断されました。\n';
        statusEl.textContent = 'CONNECTION ERROR';
        statusEl.style.color = '#f87171';
        eventSource.close();
        
        document.body.classList.remove('process-running');
        state.isRunningProcess = false;

        if (onComplete) onComplete(false);
    };
}

export function updateToggleButtonText(viewId, isShow) {
    const prefix = viewId.replace('view-', '');
    const toggleBtn = document.getElementById(`${prefix}-console-toggle`);
    if (toggleBtn) {
        toggleBtn.textContent = isShow ? '🖥️ コンソール非表示' : '🖥️ コンソール表示';
    }
}

export function toggleConsole(viewId) {
    const prefix = viewId.replace('view-', '');
    const rightPanel = document.getElementById(`${prefix}-right-panel`);
    if (rightPanel) {
        const isShow = rightPanel.classList.toggle('show');
        updateToggleButtonText(viewId, isShow);
    }
}

export function initPanelResizer(resizerId, rightPanelId) {
    const resizer = document.getElementById(resizerId);
    const rightPanel = document.getElementById(rightPanelId);
    if (!resizer || !rightPanel) return;

    resizer.addEventListener('mousedown', function(e) {
        e.preventDefault();
        resizer.classList.add('dragging');
        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    });

    function resize(e) {
        const container = resizer.parentElement;
        const containerWidth = container.clientWidth;
        const containerLeft = container.getBoundingClientRect().left;
        
        // Calculate width from the right edge
        const rightWidth = containerWidth - (e.clientX - containerLeft);
        
        // Constrain width between 300px and 70% of the viewport width
        if (rightWidth >= 300 && rightWidth <= containerWidth * 0.7) {
            rightPanel.style.width = rightWidth + 'px';
            rightPanel.style.flex = 'none'; // Override flex properties
        }
    }

    function stopResize() {
        resizer.classList.remove('dragging');
        document.removeEventListener('mousemove', resize);
        document.removeEventListener('mouseup', stopResize);
    }
}

export function confirmGlobalShutdown() { showModal('shutdown-global-modal'); }

export async function executeGlobalShutdown() {
    closeModal('shutdown-global-modal');
    try {
        await fetch('/api/shutdown', { method: 'POST' });
        window.close();
        document.body.innerHTML = `<div style="display:flex; justify-content:center; align-items:center; height:100vh; font-size:1.2rem; color:var(--text-muted)">サーバーを停止しました。ブラウザタブを閉じてください。</div>`;
    } catch (err) {
        console.error(err);
        window.close();
    }
}

export function shutdownServerGlobal() {
    confirmGlobalShutdown();
}
