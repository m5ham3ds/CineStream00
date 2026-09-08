import re

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

pattern = re.compile(r'override fun onPageFinished\(view: WebView, url: String\) \{.*?(?=\}\n\s*\}\n\s*\})', re.DOTALL)

new_code = """override fun onPageFinished(view: WebView, url: String) {
                        super.onPageFinished(view, url)
                        if (isCanceled) return
                        
                        fun injectScript() {
                            if (isCanceled || found) return
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
                    """

content = pattern.sub(new_code, content)

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
