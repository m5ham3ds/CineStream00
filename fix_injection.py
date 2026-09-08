import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Replace WebChromeClient
old_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            private var injectedForProgress = false
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                if (newProgress < 10) injectedForProgress = false
                                                if (newProgress >= 30 && !injectedForProgress) {
                                                    injectedForProgress = true
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                                // Re-inject at 80% just in case
                                                if (newProgress >= 80 && injectedForProgress && view?.tag != "injected80") {
                                                    view?.tag = "injected80"
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                            }
                                        }"""

new_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                if (newProgress >= 30) {
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                            }
                                        }"""

content = content.replace(old_chrome, new_chrome)

# Replace WebViewClient onPageStarted and onPageFinished
old_web = """                                        webViewClient = object : WebViewClient() {
                                            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                                view?.evaluateJavascript("window._aistudioScriptInjected = false;", null)
                                                super.onPageStarted(view, url, favicon)
                                                // Instantly hide WebView on navigation (e.g. after verifying CF)
                                                Handler(Looper.getMainLooper()).post {
                                                    if (bypassStatus == "CLOUDFLARE") {
                                                        bypassStatus = "CHECKING_CLOUDFLARE"
                                                    }
                                                }
                                            }

                                            override fun shouldInterceptRequest(
                                                view: WebView?,
                                                request: WebResourceRequest?
                                            ): WebResourceResponse? {
                                                val url = request?.url?.toString() ?: ""
                                                if (url.contains("google-analytics.com") || url.contains("doubleclick.net") ||
                                                    url.contains("facebook.net") || url.contains("popads.net")) {
                                                    return WebResourceResponse("text/plain", "UTF-8", null)
                                                }
                                                return super.shouldInterceptRequest(view, request)
                                            }

                                            override fun onPageFinished(view: WebView?, url: String?) {
                                                super.onPageFinished(view, url)
                                                // Injection is now handled efficiently by WebChromeClient at 70% progress
                                            }
                                        }"""

new_web = """                                        webViewClient = object : WebViewClient() {
                                            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                                super.onPageStarted(view, url, favicon)
                                                Handler(Looper.getMainLooper()).post {
                                                    if (bypassStatus == "CLOUDFLARE") {
                                                        bypassStatus = "CHECKING_CLOUDFLARE"
                                                    }
                                                }
                                            }

                                            override fun shouldInterceptRequest(
                                                view: WebView?,
                                                request: WebResourceRequest?
                                            ): WebResourceResponse? {
                                                val url = request?.url?.toString() ?: ""
                                                if (url.contains("google-analytics.com") || url.contains("doubleclick.net") ||
                                                    url.contains("facebook.net") || url.contains("popads.net")) {
                                                    return WebResourceResponse("text/plain", "UTF-8", null)
                                                }
                                                return super.shouldInterceptRequest(view, request)
                                            }

                                            override fun onPageFinished(view: WebView?, url: String?) {
                                                super.onPageFinished(view, url)
                                                val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                view?.evaluateJavascript(autoPlayScript, null)
                                                
                                                // Reinject after 1.5s to handle dynamic content loads
                                                Handler(Looper.getMainLooper()).postDelayed({
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }, 1500)
                                            }
                                        }"""

content = content.replace(old_web, new_web)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)

