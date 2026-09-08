import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_webview_client = """                                        webViewClient = object : WebViewClient() {
                                            override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                                                handler?.proceed()
                                            }"""

new_webview_client = """                                        webViewClient = object : WebViewClient() {
                                            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                                super.onPageStarted(view, url, favicon)
                                                // Instantly hide WebView on navigation (e.g. after verifying CF)
                                                Handler(Looper.getMainLooper()).post {
                                                    if (bypassStatus == "CLOUDFLARE") {
                                                        bypassStatus = "CHECKING_CLOUDFLARE"
                                                    }
                                                }
                                            }
                                            override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                                                handler?.proceed()
                                            }"""

content = content.replace(old_webview_client, new_webview_client)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
print("Dialog patched!")

