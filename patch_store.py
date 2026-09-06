import re

with open('app/src/main/java/com/example/ui/screens/player/ServerStateStore.kt', 'r') as f:
    content = f.read()

content = content.replace(
"""    var extractedServerLinks: Map<String, String> = emptyMap()""",
"""    var extractedServerLinks: Map<String, String> = emptyMap()
    var extractedServerIds: Map<String, String> = emptyMap()""")

content = content.replace(
"""        extractedServerLinks = emptyMap()""",
"""        extractedServerLinks = emptyMap()
        extractedServerIds = emptyMap()""")

with open('app/src/main/java/com/example/ui/screens/player/ServerStateStore.kt', 'w') as f:
    f.write(content)

