import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

if "import com.example.extensions.ExtensionManager" not in content:
    content = content.replace("import com.example.ui.screens.player.ServerSelectionDialog\n", "import com.example.ui.screens.player.ServerSelectionDialog\nimport com.example.extensions.ExtensionManager\nimport com.example.ui.screens.extensions.NoExtensionsDialog\n")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
