import re

def advanced_spoof(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Add extra headers to loadUrl
    content = re.sub(
        r'webView\.loadUrl\(url\)',
        'val extraHeaders = mutableMapOf<String, String>()\n                extraHeaders["Accept-Language"] = "ar,en-US;q=0.9,en;q=0.8"\n                extraHeaders["DNT"] = "1"\n                extraHeaders["Upgrade-Insecure-Requests"] = "1"\n                extraHeaders["Sec-Fetch-Dest"] = "document"\n                extraHeaders["Sec-Fetch-Mode"] = "navigate"\n                extraHeaders["Sec-Fetch-Site"] = "none"\n                extraHeaders["Sec-Fetch-User"] = "?1"\n                webView.loadUrl(url, extraHeaders)',
        content
    )
    
    # BackgroundWebView uses currentUrl instead of url
    content = re.sub(
        r'webView\.loadUrl\(currentUrl\)',
        'val extraHeaders = mutableMapOf<String, String>()\n                    extraHeaders["Accept-Language"] = "ar,en-US;q=0.9,en;q=0.8"\n                    extraHeaders["DNT"] = "1"\n                    extraHeaders["Upgrade-Insecure-Requests"] = "1"\n                    webView.loadUrl(currentUrl, extraHeaders)',
        content
    )

    # Inject navigator spoofing in onPageStarted
    spoof_js = """                        // Spoof navigator properties to evade bot detection
                        view?.evaluateJavascript(\"\"\"
                            Object.defineProperty(navigator, 'webdriver', { get: () => false });
                            Object.defineProperty(navigator, 'languages', { get: () => ['ar', 'en-US', 'en'] });
                            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                            window.chrome = { runtime: {} };
                        \"\"\".trimIndent(), null)
                        super.onPageStarted(view, url, favicon)"""
                        
    content = re.sub(r'super\.onPageStarted\(view, url, favicon\)', spoof_js, content)

    with open(file_path, 'w') as f:
        f.write(content)

advanced_spoof('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt')
advanced_spoof('app/src/main/java/com/example/ui/components/BackgroundWebView.kt')
