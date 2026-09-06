import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# We'll completely replace the autoPlayScript with a Kotlin function that generates the correct JS string
start_idx = content.find("val autoPlayScript = \"\"\"")
end_idx = content.find("})();", start_idx) + 5
end_idx = content.find("\"\"\".trimIndent()", end_idx) + 16

if start_idx != -1 and end_idx != -1:
    new_script_gen = """val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode)"""
    content = content[:start_idx] + new_script_gen + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
