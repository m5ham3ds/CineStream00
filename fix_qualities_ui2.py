import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

pattern = r'\} else if \(isExtractingQualities\) \{.*?\} else if \(extractedServers\.isNotEmpty\(\)\) \{'

new_content = re.sub(pattern, '} else if (extractedServers.isNotEmpty()) {', content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(new_content)

print("Replaced successfully.")
