import re

with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'r') as f:
    content = f.read()

# Check if onPageStarted is already there
if "onPageStarted" not in content:
    replacement = """                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }
                        
                        override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                            view?.evaluateJavascript(\"\"\"
                                Object.defineProperty(navigator, 'webdriver', { get: () => false });
                                Object.defineProperty(navigator, 'languages', { get: () => ['ar', 'en-US', 'en'] });
                                Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                                window.chrome = { runtime: {} };
                            \"\"\".trimIndent(), null)
                            super.onPageStarted(view, url, favicon)
                        }"""
    
    content = re.sub(
        r'override fun onReceivedSslError\(view: WebView\?, handler: android\.webkit\.SslErrorHandler\?, error: android\.net\.http\.SslError\?\) \{\s*handler\?\.proceed\(\)\s*\}',
        replacement,
        content
    )

    with open('app/src/main/java/com/example/ui/components/BackgroundWebView.kt', 'w') as f:
        f.write(content)
