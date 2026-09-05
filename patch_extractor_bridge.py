import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

old_interface = """                addJavascriptInterface(object {
                    @android.webkit.JavascriptInterface
                    fun sendServers(serversStr: String) {
                        val servers = serversStr.split(",").filter { it.isNotBlank() }
                        if (servers.isNotEmpty()) {
                            Handler(Looper.getMainLooper()).post {
                                onServersFound?.invoke(servers)
                            }
                        }
                    }
                }, "AndroidBridge")"""

new_interface = """                addJavascriptInterface(object {
                    @android.webkit.JavascriptInterface
                    fun sendServers(serversStr: String) {
                        val servers = serversStr.split(",").filter { it.isNotBlank() }
                        if (servers.isNotEmpty()) {
                            Handler(Looper.getMainLooper()).post {
                                onServersFound?.invoke(servers)
                            }
                        }
                    }
                    
                    @android.webkit.JavascriptInterface
                    fun sendIframeUrl(url: String) {
                        Handler(Looper.getMainLooper()).post {
                            // If we find an iframe URL, we can treat it as a video source to extract from
                            onVideoUrlFound(url)
                        }
                    }
                }, "AndroidBridge")"""

content = content.replace(old_interface, new_interface)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
