import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_block = """                    webViewClient = object : com.ead.lib.cloudflare_bypass.BypassClient() {
                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }

                        override fun onPageFinishedByPassed(view: WebView?, url: String?) {
                            super.onPageFinishedByPassed(view, url)
                            
                            val isMovieStr = if (isMovie) "true" else "false"
                            val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                            view?.evaluateJavascript(autoPlayScript, null)
                        }
                    }"""

new_block = """                    webViewClient = object : com.ead.lib.cloudflare_bypass.BypassClient() {
                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }
                        
                        override fun onPageFinished(view: WebView?, url: String?) {
                            super.onPageFinished(view, url)
                            // Inject our script immediately to report status and handle extraction, 
                            // avoiding the 15-second delay of BypassClient's onPageFinishedByPassed
                            val isMovieStr = if (isMovie) "true" else "false"
                            val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                            view?.evaluateJavascript(autoPlayScript, null)
                        }

                        override fun onPageFinishedByPassed(view: WebView?, url: String?) {
                            super.onPageFinishedByPassed(view, url)
                        }
                    }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Patched bypass successfully!")
else:
    print("Could not find block!")
