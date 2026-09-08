with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

import re

# Fix brackets at the end of webViewClient
content = content.replace("                }\n        },", "                }\n            }\n        },")

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
