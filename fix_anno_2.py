import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Fix repeated annotation
old = """                                            @android.webkit.JavascriptInterface
                                            fun logDebug(msg: String) {
                                                android.util.Log.d("AISTUDIO_DEBUG", msg)
                                            }
                                            @android.webkit.JavascriptInterface
                                            fun sendBypassStatus"""
new = """                                            @android.webkit.JavascriptInterface
                                            fun logDebug(msg: String) {
                                                android.util.Log.d("AISTUDIO_DEBUG", msg)
                                            }
                                            
                                            @android.webkit.JavascriptInterface
                                            fun sendBypassStatus"""
content = content.replace(old, new)

# Actually, I might have messed up the replacement last time. Let's just fix it by regex:
content = re.sub(r'(@android\.webkit\.JavascriptInterface\s*){2,}', '@android.webkit.JavascriptInterface\n', content)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
