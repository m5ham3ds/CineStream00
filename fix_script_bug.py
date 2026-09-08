import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Remove all occurrences of the broken injection
bad_code1 = """    if (window._aistudioScriptInjected) return;
    window._aistudioScriptInjected = true;"""
content = content.replace(bad_code1, "")

# Remove empty lines left behind if any, but it's fine.

# Let's add a much safer injection mechanism by modifying getScriptForSite and getScriptForVideoExtractor Kotlin functions themselves:
# Actually, the string literal starts with `(function() {`. We can just do a regex replace to ensure it's ONLY at the exact start.
# But wait, it's safer to just inject it properly.
# Let's just restore the file completely and carefully.

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)

