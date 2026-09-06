import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_code = """                                val serversNames = mutableListOf<String>()
                                val serversMap = mutableMapOf<String, String>()
                                
                                for (i in 0 until serversData.length()) {
                                    val item = serversData.getJSONObject(i)
                                    val name = item.getString("name")
                                    val link = item.getString("link")
                                    serversNames.add(name)
                                    serversMap[name] = link
                                }
                                
                                if (serversNames.isNotEmpty() && extractedServers.isEmpty()) {
                                    Handler(Looper.getMainLooper()).post {
                                        finalWatchUrl = url
                                        extractedServers = serversNames
                                        extractedServerLinks = serversMap // We will store this in a state
                                        com.example.ui.screens.player.ServerStateStore.extractedServers = serversNames
                                        com.example.ui.screens.player.ServerStateStore.extractedServerLinks = serversMap
                                        isLoading = false
                                    }
                                }"""

new_code = """                                val serversNames = mutableListOf<String>()
                                val serversMap = mutableMapOf<String, String>()
                                val serversIds = mutableMapOf<String, String>()
                                
                                for (i in 0 until serversData.length()) {
                                    val item = serversData.getJSONObject(i)
                                    val name = item.getString("name")
                                    val link = if (item.has("link")) item.getString("link") else ""
                                    val id = if (item.has("id")) item.getString("id") else ""
                                    serversNames.add(name)
                                    serversMap[name] = link
                                    serversIds[name] = id
                                }
                                
                                if (serversNames.isNotEmpty() && extractedServers.isEmpty()) {
                                    Handler(Looper.getMainLooper()).post {
                                        finalWatchUrl = url
                                        extractedServers = serversNames
                                        extractedServerLinks = serversMap
                                        com.example.ui.screens.player.ServerStateStore.extractedServers = serversNames
                                        com.example.ui.screens.player.ServerStateStore.extractedServerLinks = serversMap
                                        com.example.ui.screens.player.ServerStateStore.extractedServerIds = serversIds
                                        isLoading = false
                                    }
                                }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

