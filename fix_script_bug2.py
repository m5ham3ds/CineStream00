import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Replace `var intervalId = setInterval` with `window._aistudioIntervalId = setInterval`
content = content.replace("var intervalId = setInterval", "window._aistudioIntervalId = setInterval")
content = content.replace("clearInterval(intervalId)", "clearInterval(window._aistudioIntervalId)")

# At the very start of the IIFE:
# It's better to just do this:
old_start = "(function() {"
new_start = "(function() {\n    if (window._aistudioIntervalId) clearInterval(window._aistudioIntervalId);\n"

# But since we have multiple `(function() {` (maybe?), let's just do it securely.
content = content.replace(old_start, new_start)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
