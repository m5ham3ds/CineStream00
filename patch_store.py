import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Update sendServersV2
old_code = """                                        extractedServerLinks = serversMap // We will store this in a state
                                        isLoading = false"""

new_code = """                                        extractedServerLinks = serversMap // We will store this in a state
                                        com.example.ui.screens.player.ServerStateStore.extractedServers = serversNames
                                        com.example.ui.screens.player.ServerStateStore.extractedServerLinks = serversMap
                                        isLoading = false"""
content = content.replace(old_code, new_code)

# Update sendServers (old version)
old_code_2 = """                                    finalWatchUrl = url
                                    extractedServers = servers
                                    isLoading = false"""

new_code_2 = """                                    finalWatchUrl = url
                                    extractedServers = servers
                                    val tempMap = servers.associateWith { "" }
                                    com.example.ui.screens.player.ServerStateStore.extractedServers = servers
                                    com.example.ui.screens.player.ServerStateStore.extractedServerLinks = tempMap
                                    extractedServerLinks = tempMap
                                    isLoading = false"""
content = content.replace(old_code_2, new_code_2)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
