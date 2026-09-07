import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'targetServer = uiState.currentServer ?: targetServer,',
    'targetServer = if (uiState.currentServer.isNotEmpty()) uiState.currentServer else targetServer,'
)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
