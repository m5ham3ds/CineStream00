import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Fix the warning icon reference properly using Outlined instead of Default/Filled/Rounded
old_icon = "androidx.compose.material.icons.Icons.Rounded.Warning"
new_icon = "androidx.compose.material.icons.Icons.Outlined.Warning"

content = content.replace(old_icon, new_icon)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
print("Icon fixed 3!")
