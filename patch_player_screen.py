import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

# We need to find AndroidView(factory = { PlayerView(it).apply { player = exoPlayer } })
# and replace it with if/else to support WebView for iframes.

# First check if WebView is imported
if "android.webkit.WebView" not in content:
    content = "import android.webkit.WebView\nimport android.webkit.WebSettings\n" + content

# Find the AndroidView
old_android_view = """            AndroidView(
                factory = {
                    androidx.media3.ui.PlayerView(it).apply {
                        player = exoPlayer
                        useController = true
                        setShowNextButton(false)
                        setShowPreviousButton(false)
                        layoutParams = android.view.ViewGroup.LayoutParams(
                            android.view.ViewGroup.LayoutParams.MATCH_PARENT,
                            android.view.ViewGroup.LayoutParams.MATCH_PARENT
                        )
                    }
                },
                modifier = Modifier.fillMaxSize()
            )"""

new_android_view = """            if (uiState.currentVideoUrl?.let { it.endsWith(".m3u8") || it.endsWith(".mp4") || it.endsWith(".mkv") || (it.startsWith("http") && it.contains("videodelivery.net")) } == true) {
                AndroidView(
                    factory = {
                        androidx.media3.ui.PlayerView(it).apply {
                            player = exoPlayer
                            useController = true
                            setShowNextButton(false)
                            setShowPreviousButton(false)
                            layoutParams = android.view.ViewGroup.LayoutParams(
                                android.view.ViewGroup.LayoutParams.MATCH_PARENT,
                                android.view.ViewGroup.LayoutParams.MATCH_PARENT
                            )
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
            } else {
                AndroidView(
                    factory = { ctx ->
                        WebView(ctx).apply {
                            settings.javaScriptEnabled = true
                            settings.domStorageEnabled = true
                            settings.mediaPlaybackRequiresUserGesture = false
                            settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                            layoutParams = android.view.ViewGroup.LayoutParams(
                                android.view.ViewGroup.LayoutParams.MATCH_PARENT,
                                android.view.ViewGroup.LayoutParams.MATCH_PARENT
                            )
                            uiState.currentVideoUrl?.let { loadUrl(it) }
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )
            }"""

if old_android_view in content:
    content = content.replace(old_android_view, new_android_view)
else:
    print("Could not find the exact old AndroidView block.")

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)

print("PlayerScreen patched.")
