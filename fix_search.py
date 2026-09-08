import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

content = content.replace("replace(/[^a-z0-9]/gi, ' ')", "replace(/[^a-z0-9\\u0600-\\u06FF]/gi, ' ')")

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
