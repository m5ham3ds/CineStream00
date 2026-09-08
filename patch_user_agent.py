import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_block = """                        javaScriptCanOpenWindowsAutomatically = true
                        userAgentString = WebSettings.getDefaultUserAgent(ctx)
                        mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW"""

new_block = """                        javaScriptCanOpenWindowsAutomatically = true
                        userAgentString = "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
                        mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Patched UserAgent successfully!")
else:
    print("Could not find UserAgent block!")
