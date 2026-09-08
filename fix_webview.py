import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Add WebChromeClient
old_webviewclient = """                                        webViewClient = object : WebViewClient() {"""
new_webviewclient = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                if (newProgress >= 70) {
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                            }
                                        }
                                        webViewClient = object : WebViewClient() {"""

content = content.replace(old_webviewclient, new_webviewclient)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
