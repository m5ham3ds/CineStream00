import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_click = """                                    .clickable {
                                        selectedServerToExtract = server
                                        selectedServerUrlToExtract = extractedServerLinks[server] ?: finalWatchUrl ?: searchUrl
                                        availableQualities = emptyList()
                                        isExtractingQualities = true
                                    },"""

new_click = """                                    .clickable {
                                        val urlToPlay = extractedServerLinks[server] ?: finalWatchUrl ?: searchUrl
                                        onPlay(urlToPlay, server, currentSiteName)
                                    },"""

if old_click in content:
    content = content.replace(old_click, new_click)
    print("Replaced successfully.")
else:
    print("old_click not found!")

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

