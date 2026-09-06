import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_code = """        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            isAnime = isAnime,
            title = initialTitle,
            availableWebsites = availableList,
            currentWebsite = bestWebsite,
            fallbackWebsites = remainingFallbacks,
            currentServer = targetServer ?: ""
        )"""

new_code = """        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            isAnime = isAnime,
            title = initialTitle,
            availableWebsites = availableList,
            currentWebsite = bestWebsite,
            fallbackWebsites = remainingFallbacks,
            currentServer = targetServer ?: "",
            availableServers = com.example.ui.screens.player.ServerStateStore.extractedServers,
            availableServerLinks = com.example.ui.screens.player.ServerStateStore.extractedServerLinks
        )"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
