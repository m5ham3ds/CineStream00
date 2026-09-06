import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_code = """    fun setExtractedUrl(url: String) {
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

new_code = """    fun setFinalVideoUrl(url: String) {
        extractionTimeoutJob?.cancel()
        if (_uiState.value.currentVideoUrl != url) {
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = url,
                isLoading = false
            )
        }
    }

    fun setIframeUrl(url: String) {
        extractionTimeoutJob?.cancel()
        _uiState.value = _uiState.value.copy(
            extractionUrl = url,
            isLoading = true,
            currentVideoUrl = null
        )
        startExtractionTimeout()
    }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)

