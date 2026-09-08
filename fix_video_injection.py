import re

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

old_web = """                    override fun onPageFinished(view: WebView?, url: String?) {
                        super.onPageFinished(view, url)
                        if (isCanceled) return
                        if (!found && url != null) {
                            val script = SiteScripts.getScriptForVideoExtractor(url, serverId)
                            view?.evaluateJavascript(script, null)
                        }
                    }"""

new_web = """                    override fun onPageFinished(view: WebView?, url: String?) {
                        super.onPageFinished(view, url)
                        if (isCanceled) return
                        if (!found && url != null) {
                            val script = SiteScripts.getScriptForVideoExtractor(url, serverId)
                            view?.evaluateJavascript(script, null)
                            
                            // Re-inject dynamically
                            Handler(Looper.getMainLooper()).postDelayed({
                                if (!found) view?.evaluateJavascript(script, null)
                            }, 2000)
                        }
                    }"""

content = content.replace(old_web, new_web)

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
