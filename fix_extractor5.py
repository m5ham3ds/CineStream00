import re

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

content = content.replace("if (isCanceled) return\n", "")
content = content.replace("if (isCanceled || found) return", "if (found) return")

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
