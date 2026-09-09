with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

if "import androidx.compose.animation.togetherWith" not in content:
    content = content.replace("package com.example.ui.screens.player\n", "package com.example.ui.screens.player\n\nimport androidx.compose.animation.togetherWith\n")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
