import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

start_idx = content.find("val autoPlayScript = \"\"\"")
end_idx = content.find("})();", start_idx) + 5
end_idx = content.find("\"\"\".trimIndent()", end_idx) + 16

if start_idx != -1 and end_idx != -1:
    new_script_gen = """val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url)"""
    content = content[:start_idx] + new_script_gen + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
