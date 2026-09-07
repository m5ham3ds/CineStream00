import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

replacement = """    fun selectWebsite(website: String) {
        com.example.ui.screens.player.ServerStateStore.clear()
        _uiState.value = _uiState.value.copy(
            currentWebsite = website, 
            isLoading = true, 
            currentVideoUrl = null, 
            fallbackWebsites = emptyList(),
            availableServers = emptyList(),
            availableServerLinks = emptyMap(),
            availableServerIds = emptyMap(),
            currentServer = ""
        )
        generateExtractionUrl()
    }"""

content = re.sub(r'    fun selectWebsite\(website: String\) \{.*generateExtractionUrl\(\)\n    \}', replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
