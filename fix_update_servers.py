import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

replacement = """    fun updateServers(servers: List<String>) {
        if (_uiState.value.availableServers != servers && servers.isNotEmpty()) {
            val firstServer = servers.first()
            val link = com.example.ui.screens.player.ServerStateStore.extractedServerLinks[firstServer]
            val id = com.example.ui.screens.player.ServerStateStore.extractedServerIds[firstServer]
            
            var nextExtractionUrl = _uiState.value.extractionUrl
            if (link != null && link.isNotEmpty()) {
                nextExtractionUrl = link
            }
            
            _uiState.value = _uiState.value.copy(
                availableServers = servers,
                currentServer = firstServer,
                extractionUrl = nextExtractionUrl,
                serverIdToChange = id
            )
            
            if (nextExtractionUrl != null) {
                startExtractionTimeout()
            }
        }
    }"""

content = re.sub(r'    fun updateServers\(servers: List<String>\) \{.*?\n    \}', replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
