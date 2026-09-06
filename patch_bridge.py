import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

content = content.replace(
"""fun HiddenVideoExtractor(
    url: String,
    isMovie: Boolean = true,
    season: Int = 1,
    episode: Int = 1,
    targetServer: String? = null,
    onVideoUrlFound: (String) -> Unit,
    onServersFound: ((List<String>) -> Unit)? = null
)""",
"""fun HiddenVideoExtractor(
    url: String,
    isMovie: Boolean = true,
    season: Int = 1,
    episode: Int = 1,
    targetServer: String? = null,
    onVideoUrlFound: (String) -> Unit,
    onIframeUrlFound: ((String) -> Unit)? = null,
    onServersFound: ((List<String>) -> Unit)? = null
)""")

content = content.replace(
"""                    @android.webkit.JavascriptInterface
                    fun sendIframeUrl(url: String) {
                        Handler(Looper.getMainLooper()).post {
                            // If we find an iframe URL, we can treat it as a video source to extract from
                            onVideoUrlFound(url)
                        }
                    }""",
"""                    @android.webkit.JavascriptInterface
                    fun sendIframeUrl(url: String) {
                        Handler(Looper.getMainLooper()).post {
                            onIframeUrlFound?.invoke(url) ?: onVideoUrlFound(url)
                        }
                    }""")

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)

