with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

import re

# Let's replace the whole webViewClient section
pattern = re.compile(r'webViewClient = object : WebViewClient\(\) \{.*?(?=\}\n\s*update = \{)', re.DOTALL)

new_client = """webViewClient = object : WebViewClient() {
                    var found = false

                    override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                        handler?.proceed()
                    }

                    override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                        found = false
                        // Spoof navigator properties to evade bot detection
                        view?.evaluateJavascript(\"\"\"
                            Object.defineProperty(navigator, 'webdriver', { get: () => false });
                            Object.defineProperty(navigator, 'languages', { get: () => ['ar', 'en-US', 'en'] });
                            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
                            window.chrome = { runtime: {} };
                        \"\"\".trimIndent(), null)
                        super.onPageStarted(view, url, favicon)
                    }

                    override fun shouldInterceptRequest(
                        view: WebView?,
                        request: WebResourceRequest?
                    ): WebResourceResponse? {
                        val reqUrl = request?.url.toString()
                        
                        // Look for standard streaming formats
                        if (!found && (reqUrl.contains(".m3u8") || reqUrl.contains(".mp4") || reqUrl.contains(".mkv") || reqUrl.contains("videodelivery.net") || reqUrl.contains("v.mp4"))) {
                            // Avoid common ad scripts that might have these strings
                            if (!reqUrl.contains("adsystem") && !reqUrl.contains("tracker") && !reqUrl.contains("googleads") && !reqUrl.contains("facebook") && !reqUrl.contains("tiktok")) {
                                found = true
                                Handler(Looper.getMainLooper()).post {
                                    onVideoUrlFound(reqUrl)
                                }
                            }
                        }
                        
                        return super.shouldInterceptRequest(view, request)
                    }

                    override fun onPageFinished(view: WebView, url: String) {
                        super.onPageFinished(view, url)
                        
                        fun injectScript() {
                            if (found) return
                            if (com.example.ui.screens.player.ServerStateStore.extractedServers.isEmpty()) {
                                val siteScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(
                                    website, 
                                    isMovie, 
                                    episode, 
                                    title
                                )
                                view.evaluateJavascript(siteScript, null)
                            } else {
                                val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url, targetServerId)
                                view.evaluateJavascript(autoPlayScript, null)
                            }
                        }
                        
                        injectScript()
                        
                        // Hybrid polling: keep injecting every 1.5s for up to 15s in case of AJAX loading
                        for (i in 1..10) {
                            Handler(Looper.getMainLooper()).postDelayed({
                                injectScript()
                            }, i * 1500L)
                        }
                    }
                }
            }
        """

content = pattern.sub(new_client, content)

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
