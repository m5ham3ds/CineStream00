import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# 1. Update WebViewClient
old_client_start = "webViewClient = object : WebViewClient() {"
old_client_end = "                                        }\n                                    }\n                                },"

# We will just replace everything between these.
pattern = re.compile(r'webViewClient = object : WebViewClient\(\) \{.*?\n\s*\}\n\s*\}\n\s*\},', re.DOTALL)

new_client = """webViewClient = object : WebViewClient() {
                                            private var isNotified = false
                                            private var urlToCheck = ""
                                            private var checkAttempt = 0

                                            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                                super.onPageStarted(view, url, favicon)
                                                isNotified = false
                                                checkAttempt = 0
                                                Handler(Looper.getMainLooper()).post {
                                                    if (bypassStatus == "CLOUDFLARE") {
                                                        bypassStatus = "CHECKING_CLOUDFLARE"
                                                    }
                                                }
                                            }

                                            override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                                                handler?.proceed()
                                            }

                                            override fun onReceivedError(view: WebView?, request: android.webkit.WebResourceRequest?, error: android.webkit.WebResourceError?) {
                                                super.onReceivedError(view, request, error)
                                                if (request?.isForMainFrame == true) {
                                                    val errorCode = error?.errorCode ?: 0
                                                    if (errorCode == android.webkit.WebViewClient.ERROR_HOST_LOOKUP || 
                                                        errorCode == android.webkit.WebViewClient.ERROR_CONNECT || 
                                                        errorCode == android.webkit.WebViewClient.ERROR_TIMEOUT) {
                                                        Handler(Looper.getMainLooper()).post {
                                                            isNetworkError = true
                                                        }
                                                    }
                                                }
                                            }

                                            private fun repeatCheck(view: WebView?, attempt: Int) {
                                                if (attempt > 30 || isNotified) return // Max 30 seconds

                                                val checkJS = \"\"\"
                                                    (function() {
                                                        var urlChanged = window.location.href.indexOf('cf_chl') === -1 && 
                                                                         window.location.href.indexOf('challenge') === -1 &&
                                                                         window.location.href.indexOf('__cf') === -1;

                                                        var challengeExists = document.getElementById('challenge-running') !== null ||
                                                                              document.querySelector('.cf-browser-verification') !== null ||
                                                                              document.body.innerText.indexOf('Checking your browser') !== -1 ||
                                                                              document.title.toLowerCase().indexOf('just a moment') !== -1;

                                                        var contentExists = document.querySelector('video') !== null ||
                                                                            document.querySelector('.download-btn') !== null ||
                                                                            document.getElementById('player-container') !== null ||
                                                                            document.querySelector('iframe') !== null ||
                                                                            document.querySelector('a') !== null;

                                                        return (urlChanged || !challengeExists) && contentExists;
                                                    })();
                                                \"\"\".trimIndent()

                                                view?.evaluateJavascript(checkJS) { result ->
                                                    if (result == "true" && !isNotified) {
                                                        isNotified = true
                                                        
                                                        // Bypass successful!
                                                        Handler(Looper.getMainLooper()).post {
                                                            android.webkit.CookieManager.getInstance().flush()
                                                            bypassStatus = "NORMAL"
                                                        }

                                                        // Inject extraction script now that we know we bypassed
                                                        val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                        view?.evaluateJavascript(autoPlayScript, null)
                                                    } else {
                                                        // Schedule next check
                                                        Handler(Looper.getMainLooper()).postDelayed({
                                                            repeatCheck(view, attempt + 1)
                                                        }, 1000)
                                                    }
                                                }
                                            }

                                            override fun onPageFinished(view: WebView?, url: String?) {
                                                super.onPageFinished(view, url)
                                                if (url == null || isNotified) return
                                                urlToCheck = url
                                                
                                                // Always inject at least once just in case it's a direct load
                                                val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                view?.evaluateJavascript(autoPlayScript, null)

                                                repeatCheck(view, 0)
                                            }
                                        }
                                    }
                                },"""

content = pattern.sub(new_client, content)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
