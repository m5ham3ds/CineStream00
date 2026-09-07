import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'targetServer = if (uiState.currentServer.isNotEmpty()) uiState.currentServer else targetServer,',
    'targetServer = uiState.currentServer.ifEmpty { null },'
)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
