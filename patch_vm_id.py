import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_code = """    fun selectServer(server: String) {
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

# If link is present but id is ALSO present, we need to pass the id and the link!
# Wait, if link == window.location.href, we can just pass link to extractionUrl and id to serverIdToChange!
new_code = """    fun selectServer(server: String) {
        val link = _uiState.value.availableServerLinks[server]
        val id = _uiState.value.availableServerIds[server]
        
        var nextExtractionUrl = _uiState.value.extractionUrl
        if (link != null && link.isNotEmpty()) {
            nextExtractionUrl = link
        }
        
        _uiState.value = _uiState.value.copy(
            currentServer = server,
            isLoading = true,
            currentVideoUrl = null,
            extractionUrl = nextExtractionUrl,
            serverIdToChange = id
        )
        
        if (nextExtractionUrl != null) {
            startExtractionTimeout()
        } else {
            generateExtractionUrl()
        }
    }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)

