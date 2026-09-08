import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                if (newProgress >= 30) {
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                            }
                                        }"""
new_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
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
content = content.replace(old_chrome, new_chrome)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
