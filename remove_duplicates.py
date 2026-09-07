import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

# Replace the block from lines 94 to 112 (the duplicate functions)
to_remove = """
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

content = content.replace(to_remove, "", 1) # only replace the first occurrence (or just replace exactly what we need)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)

