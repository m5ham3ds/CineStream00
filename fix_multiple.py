import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                if (newProgress >= 70) {
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                            }
                                        }"""
new_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
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

content = content.replace(old_chrome, new_chrome)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
