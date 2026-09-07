import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

replacement = """                    override fun onPageFinished(view: WebView, url: String) {
                        super.onPageFinished(view, url)
                        // If we don't have servers, we need to extract them first!
                        if (com.example.ui.screens.player.ServerStateStore.extractedServers.isEmpty()) {
                            val siteScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(
                                com.example.utils.UrlHelper.getDomainName(url), 
                                isMovie, 
                                episode, 
                                ""
                            )
                            view.evaluateJavascript(siteScript, null)
                        } else {
                            // Inject script to automatically click play buttons to force stream load
                            val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url, targetServerId)
                            view.evaluateJavascript(autoPlayScript, null)
                        }
                    }"""

content = re.sub(r'                    override fun onPageFinished\(view: WebView, url: String\) \{.*?\n                    \}', replacement, content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
