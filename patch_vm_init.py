import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_code = """            availableServers = com.example.ui.screens.player.ServerStateStore.extractedServers,
            availableServerLinks = com.example.ui.screens.player.ServerStateStore.extractedServerLinks
        )"""

new_code = """            availableServers = com.example.ui.screens.player.ServerStateStore.extractedServers,
            availableServerLinks = com.example.ui.screens.player.ServerStateStore.extractedServerLinks,
            availableServerIds = com.example.ui.screens.player.ServerStateStore.extractedServerIds
        )"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)

