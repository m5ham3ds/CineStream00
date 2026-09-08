import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Let's clean out ALL the injected garbage at the start of functions
content = re.sub(r'    if \(window\._aistudioIntervalId\)\s*clearInterval\(window\._aistudioIntervalId\);\n+', '', content)
content = re.sub(r'    if \(window\._aistudioScriptInjected\)\s*return;\n\s*window\._aistudioScriptInjected = true;\n+', '', content)

# Now, we manually inject it AT THE VERY START of the string literals.
# The string literals start with `        (function() {`

def replace_iife_start(match):
    return match.group(0) + "\n            if (window._aistudioIntervalId) clearInterval(window._aistudioIntervalId);\n"

content = re.sub(r'\(\s*function\s*\(\)\s*\{', replace_iife_start, content)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)

