import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Replace with an icon we know is imported and works (e.g. Close, or just remove the icon)
old_icon = "androidx.compose.material.icons.Icons.Default.Info"
new_icon = "androidx.compose.material.icons.Icons.Default.Close"

content = content.replace(old_icon, new_icon)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
print("Icon fixed 5!")
