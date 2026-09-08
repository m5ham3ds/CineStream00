import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Add a check at the beginning of the IIFE
content = content.replace("(function() {", "(function() {\n    if (window._aistudioScriptInjected) return;\n    window._aistudioScriptInjected = true;\n")

# In ServerSelectionDialog, we want to reset window._aistudioScriptInjected on page start!
with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    dialog = f.read()

old_start = """                                            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {"""
new_start = """                                            override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                                view?.evaluateJavascript("window._aistudioScriptInjected = false;", null)"""

dialog = dialog.replace(old_start, new_start)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(dialog)

# Also fix the JS detection in VideoExtractor.kt inside SiteScripts.kt
old_detect_2 = """                var isCloudflare = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');"""
new_detect_2 = """                var title = document.title.toLowerCase();
                var bodyText = document.body ? document.body.innerText.toLowerCase() : "";
                var isCloudflare = title.includes('just a moment') || title.includes('cloudflare') || title.includes('attention required') || 
                                   bodyText.includes('security verification') || bodyText.includes('malicious bots') || 
                                   bodyText.includes('not a bot') || bodyText.includes('يتم التحقق') || bodyText.includes('cloudflare');"""

content = content.replace(old_detect_2, new_detect_2)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)

