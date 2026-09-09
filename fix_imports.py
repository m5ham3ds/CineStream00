with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

if "import com.example.extensions.ExtensionManager" not in content:
    content = content.replace("package com.example.ui.screens.player\n", "package com.example.ui.screens.player\n\nimport com.example.extensions.ExtensionManager\n")

if "import com.example.extensions.ProviderExtension" not in content:
    content = content.replace("package com.example.ui.screens.player\n", "package com.example.ui.screens.player\n\nimport com.example.extensions.ProviderExtension\n")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
