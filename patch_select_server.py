import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_code = """    fun selectServer(server: String) {
        _uiState.value = _uiState.value.copy(currentServer = server, isLoading = true, currentVideoUrl = null)
        generateExtractionUrl() // In a real app, this might change the iframe URL params
    }"""

new_code = """    fun selectServer(server: String) {
        val link = _uiState.value.availableServerLinks[server]
        val id = _uiState.value.availableServerIds[server]
        if (link != null && link.isNotEmpty()) {
            _uiState.value = _uiState.value.copy(
                currentServer = server,
                isLoading = true,
                currentVideoUrl = null,
                extractionUrl = link
            )
            startExtractionTimeout()
        } else if (id != null && id.isNotEmpty()) {
            _uiState.value = _uiState.value.copy(
                currentServer = server,
                isLoading = true,
                currentVideoUrl = null,
                serverIdToChange = id
            )
            generateExtractionUrl()
        } else {
            _uiState.value = _uiState.value.copy(
                currentServer = server,
                isLoading = true,
                currentVideoUrl = null
            )
            generateExtractionUrl()
        }
    }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
