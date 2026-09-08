import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Remove the delayed injection from onPageFinished
old_onpagefinished = """                                            override fun onPageFinished(view: WebView?, url: String?) {
                                                super.onPageFinished(view, url)
                                                // Wait a short moment to ensure DOM is ready, then inject
                                                Handler(Looper.getMainLooper()).postDelayed({
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }, 1000)
                                            }"""
new_onpagefinished = """                                            override fun onPageFinished(view: WebView?, url: String?) {
                                                super.onPageFinished(view, url)
                                                // Injection is now handled efficiently by WebChromeClient at 70% progress
                                            }"""

content = content.replace(old_onpagefinished, new_onpagefinished)

# Make scriptInjected accessible to both clients
# Wait, let's just use evaluateJavascript inside WebChromeClient but reset it in a clever way.
# Or just reset it when url changes.
# Actually, I'll just change WebChromeClient to:
old_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            private var scriptInjected = false
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                if (newProgress >= 70 && !scriptInjected) {
                                                    scriptInjected = true
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                                if (newProgress < 10) {
                                                    scriptInjected = false // Reset on new page load
                                                }
                                            }
                                        }"""
new_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            private var scriptInjectedUrl = ""
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                val currentUrl = view?.url ?: ""
                                                if (newProgress >= 60 && scriptInjectedUrl != currentUrl) {
                                                    scriptInjectedUrl = currentUrl
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                            }
                                        }"""

content = content.replace(old_chrome, new_chrome)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
