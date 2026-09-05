import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_func = """    fun setExtractedUrl(url: String) {
        extractionTimeoutJob?.cancel()
        // Only set if we don't already have one, or if it's a new quality selection
        if (_uiState.value.currentVideoUrl != url) {
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = url,
                isLoading = false
            )
        }
    }"""

new_func = """    fun setExtractedUrl(url: String) {
        extractionTimeoutJob?.cancel()
        // If it's an iframe/embed URL, treat it as an intermediate extraction source
        if (url.contains("iframe") || url.contains("embed") || url.contains("/player/") || url.contains("megamax.me")) {
            _uiState.value = _uiState.value.copy(
                extractionUrl = url,
                isLoading = true,
                currentVideoUrl = null
            )
            startExtractionTimeout()
        } else if (_uiState.value.currentVideoUrl != url) {
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = url,
                isLoading = false
            )
        }
    }"""

content = content.replace(old_func, new_func)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)

