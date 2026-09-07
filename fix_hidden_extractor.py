import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

replacement = """                    @android.webkit.JavascriptInterface
                    fun sendServers(serversStr: String) {
                        val servers = serversStr.split(",").filter { it.isNotBlank() }
                        if (servers.isNotEmpty()) {
                            Handler(Looper.getMainLooper()).post {
                                onServersFound?.invoke(servers)
                            }
                        }
                    }

                    @android.webkit.JavascriptInterface
                    fun sendServersV2(serversJson: String, url: String) {
                        try {
                            val serversData = org.json.JSONArray(serversJson)
                            val serversNames = mutableListOf<String>()
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
                            
                            if (serversNames.isNotEmpty()) {
                                Handler(Looper.getMainLooper()).post {
                                    com.example.ui.screens.player.ServerStateStore.extractedServers = serversNames
                                    com.example.ui.screens.player.ServerStateStore.extractedServerLinks = serversMap
                                    com.example.ui.screens.player.ServerStateStore.extractedServerIds = serversIds
                                    onServersFound?.invoke(serversNames)
                                }
                            }
                        } catch (e: Exception) { e.printStackTrace() }
                    }"""

content = re.sub(r'                    @android\.webkit\.JavascriptInterface\n                    fun sendServers\(serversStr: String\) \{.*?\n                    \}', replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
