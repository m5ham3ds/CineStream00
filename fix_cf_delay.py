import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_logic = """                                                // Instantly hide WebView on navigation (e.g. after verifying CF)
                                                Handler(Looper.getMainLooper()).post {
                                                    if (bypassStatus == "CLOUDFLARE") {
                                                        bypassStatus = "CHECKING_CLOUDFLARE"
                                                    }
                                                }"""

new_logic = """                                                // Instantly hide WebView on navigation (e.g. after verifying CF)
                                                Handler(Looper.getMainLooper()).post {
                                                    if (bypassStatus == "CLOUDFLARE") {
                                                        bypassStatus = "CHECKING_CLOUDFLARE"
                                                    }
                                                }"""

content = content.replace(old_logic, new_logic)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
