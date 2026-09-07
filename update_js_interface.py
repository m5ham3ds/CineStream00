import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

# We need to add `sendFailed()`, `sendVideoUrl(url)`, and `sendBypassStatus(status)` to the JavascriptInterface

new_methods = """
                    @android.webkit.JavascriptInterface
                    fun sendVideoUrl(url: String) {
                        Handler(Looper.getMainLooper()).post {
                            onVideoUrlFound(url)
                        }
                    }
                    
                    @android.webkit.JavascriptInterface
                    fun sendFailed() {
                        // We could handle this by emitting null, but VideoExtractor just stops.
                        // We might want to pass a callback or just do nothing.
                    }
                    
                    @android.webkit.JavascriptInterface
                    fun sendBypassStatus(status: String) {
                        // Log or handle Cloudflare bypass status
                    }
"""

# Insert before sendServers
content = content.replace("@android.webkit.JavascriptInterface\n                    fun sendServers", new_methods + "                    @android.webkit.JavascriptInterface\n                    fun sendServers")

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)

