export const state = {
    isRunningProcess: false,
    novelLines: [],
    findings: [],
    activeCategoryFilter: 'all',
    activeSeverityFilter: 'all',
    activeHighlightLine: null,
    selectedNovelFile: localStorage.getItem('selectedNovelFile') || ""
};

export function setSelectedNovelFile(file) {
    state.selectedNovelFile = file;
    localStorage.setItem('selectedNovelFile', file);
}
