import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Make sure it's initialized correctly
if 'var bypassStatus by remember { mutableStateOf("NORMAL") }' in content:
    content = content.replace('var bypassStatus by remember { mutableStateOf("NORMAL") }', 'var bypassStatus by remember { mutableStateOf("CHECKING_CLOUDFLARE") }')
    print("Changed init to CHECKING_CLOUDFLARE")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
