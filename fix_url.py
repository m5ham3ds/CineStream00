import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

bad_str = "val targetUrl = com.example.ui.screens.player.SiteScripts.getSiteUrl(currentSiteName, isMovie, title, season, episode)"
good_str = "val targetUrl = searchUrl"

content = content.replace(bad_str, good_str)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
