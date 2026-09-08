import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Fix Cloudflare detection
old_detect = """                var isCloudflareTitle = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                var bodyText = document.body ? document.body.innerText : "";
                var isCloudflareText = bodyText.includes('Performing security verification') || bodyText.includes('protect against malicious bots') || bodyText.includes('verifies you are not a bot');
                var isCloudflare = isCloudflareTitle || isCloudflareText;"""

new_detect = """                var title = document.title.toLowerCase();
                var bodyText = document.body ? document.body.innerText.toLowerCase() : "";
                var isCloudflare = title.includes('just a moment') || title.includes('cloudflare') || title.includes('attention required') || 
                                   bodyText.includes('security verification') || bodyText.includes('malicious bots') || 
                                   bodyText.includes('not a bot') || bodyText.includes('يتم التحقق') || bodyText.includes('cloudflare');"""

content = content.replace(old_detect, new_detect)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    dialog = f.read()

# Modify the WebChromeClient to inject script and also check in onPageFinished
old_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
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

# We remove the scriptInjectedUrl entirely, because JS now handles duplication with !window._scriptRun
new_chrome = """                                        webChromeClient = object : android.webkit.WebChromeClient() {
                                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                super.onProgressChanged(view, newProgress)
                                                if (newProgress >= 30) {
                                                    val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                    view?.evaluateJavascript(autoPlayScript, null)
                                                }
                                            }
                                        }"""

dialog = dialog.replace(old_chrome, new_chrome)

# Modify Box to show during CHECKING_CLOUDFLARE too, just in case, but alpha 0.01f so it loads properly?
old_box = """                                modifier = if (bypassStatus == "CLOUDFLARE") 
                                    Modifier.width(320.dp).height(150.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp))
                                else 
                                    Modifier.size(1.dp).alpha(0f),"""

new_box = """                                modifier = if (bypassStatus == "CLOUDFLARE" || bypassStatus == "CHECKING_CLOUDFLARE") 
                                    Modifier.width(320.dp).height(150.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp)).alpha(if (bypassStatus == "CLOUDFLARE") 1f else 0.01f)
                                else 
                                    Modifier.size(1.dp).alpha(0f),"""

dialog = dialog.replace(old_box, new_box)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(dialog)
