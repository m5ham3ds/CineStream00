import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_reset = """                                    currentSiteIndex++
                                    currentSiteName = prioritySites[currentSiteIndex]
                                    extractedServers = emptyList()
                                    extractedServerLinks = emptyMap()
                                    isLoading = true
                                    isFailed = false"""

new_reset = """                                    currentSiteIndex++
                                    currentSiteName = prioritySites[currentSiteIndex]
                                    extractedServers = emptyList()
                                    extractedServerLinks = emptyMap()
                                    isLoading = true
                                    isFailed = false
                                    bypassStatus = "CHECKING_CLOUDFLARE\""""

if old_reset in content and new_reset not in content:
    content = content.replace(old_reset, new_reset)
    print("Added bypassStatus reset to site change.")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
