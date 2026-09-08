import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Fix repeated annotation
old = """                                            @android.webkit.JavascriptInterface
                                            @android.webkit.JavascriptInterface
                                            fun sendBypassStatus"""
new = """                                            @android.webkit.JavascriptInterface
                                            fun sendBypassStatus"""
content = content.replace(old, new)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
