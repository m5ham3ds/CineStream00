import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

content = content.replace(
'''                                            .clickable {
                                                val serverAndQuality = "$selectedServerForQuality - ${quality.name}"
                                                onPlay(quality.url, serverAndQuality, currentSiteName)
                                            },''', 
'''                                            .clickable {
                                                val serverNameOnly = selectedServerForQuality ?: "سيرفر"
                                                onPlay(quality.url, serverNameOnly, currentSiteName)
                                            },''')

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
