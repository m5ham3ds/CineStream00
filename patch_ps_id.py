import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

content = content.replace("targetServer = uiState.currentServer ?: targetServer,", "targetServer = uiState.currentServer ?: targetServer,\n                    targetServerId = uiState.serverIdToChange,")

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)

