import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Fix normTarget check
old_code = """                    if (results.length > 0) {
                        var targetResult = null;"""

new_code = """                    if (results.length > 0 && normTarget.length > 0) {
                        var targetResult = null;"""

content = content.replace(old_code, new_code)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
