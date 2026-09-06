import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

content = content.replace("var e = ${episode}.toString();", "var e = '${episode}';")

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)

