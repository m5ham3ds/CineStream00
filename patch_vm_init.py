import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

# Let's see how currentVideoUrl is managed when picking a server.
content = content.replace(
"""    fun selectServer(server: String) {
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
    }""",
"""    fun selectServer(server: String) {
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
    }""")

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)

