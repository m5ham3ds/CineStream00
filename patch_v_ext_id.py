import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

# Add targetServerId parameter
content = content.replace("targetServer: String? = null,", "targetServer: String? = null,\n    targetServerId: String? = null,")

content = content.replace(
    "val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url)",
    "val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url, targetServerId)"
)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)

