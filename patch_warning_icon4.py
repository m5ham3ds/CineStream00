import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Replace Warning with Info which is safely in the standard Icons set
old_icon = "androidx.compose.material.icons.Icons.Outlined.Warning"
new_icon = "androidx.compose.material.icons.Icons.Default.Info"

content = content.replace(old_icon, new_icon)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
print("Icon fixed 4!")
