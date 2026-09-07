import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'targetServerId = uiState.serverIdToChange,',
    'targetServerId = uiState.serverIdToChange,\n                    website = uiState.currentWebsite,'
)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
