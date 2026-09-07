import re

def spoof_webview(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Find the settings.apply block
    # We will replace the userAgentString logic
    
    spoof_settings = """                    // Advanced spoofing to look like a real Chrome browser
                    javaScriptEnabled = true
                    domStorageEnabled = true
                    databaseEnabled = true
                    javaScriptCanOpenWindowsAutomatically = true
                    mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                    cacheMode = WebSettings.LOAD_DEFAULT
                    mediaPlaybackRequiresUserGesture = false
                    
                    setSupportZoom(true)
                    builtInZoomControls = true
                    displayZoomControls = false
                    useWideViewPort = true
                    loadWithOverviewMode = true
                    allowFileAccess = true
                    allowContentAccess = true

                    val originalUserAgent = WebSettings.getDefaultUserAgent(ctx)
                    userAgentString = originalUserAgent.replace("; wv", "").replace("Version/4.0 ", "")"""

    # We need to replace the content inside settings.apply { ... }
    # Let's just use regex to replace from 'settings.apply {' to '}' but we need to be careful with nested brackets.
    # Actually, let's just replace the specific lines we know are there.
    
    if "userAgentString = originalUserAgent" not in content:
        content = re.sub(
            r'userAgentString = WebSettings\.getDefaultUserAgent\(ctx\)',
            'val originalUserAgent = WebSettings.getDefaultUserAgent(ctx)\n                    userAgentString = originalUserAgent.replace("; wv", "").replace("Version/4.0 ", "")\n                    setSupportZoom(true)\n                    builtInZoomControls = true\n                    displayZoomControls = false\n                    useWideViewPort = true\n                    loadWithOverviewMode = true\n                    allowFileAccess = true\n                    allowContentAccess = true',
            content
        )
    
    with open(file_path, 'w') as f:
        f.write(content)

spoof_webview('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt')
spoof_webview('app/src/main/java/com/example/ui/components/BackgroundWebView.kt')
