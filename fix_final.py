import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Strip out all injected clears first
content = re.sub(r'\s*if \(window\._aistudioIntervalId\) clearInterval\(window\._aistudioIntervalId\);', '', content)

# Now, we only inject after exactly `return """\n        (function() {`
content = content.replace('return """\n        (function() {', 'return """\n        (function() {\n            if (window._aistudioIntervalId) clearInterval(window._aistudioIntervalId);')

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
