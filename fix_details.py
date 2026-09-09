import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

if "import com.example.extensions.ExtensionManager" not in content:
    content = content.replace("import androidx.compose.ui.unit.sp", "import androidx.compose.ui.unit.sp\nimport com.example.extensions.ExtensionManager\nimport com.example.ui.screens.extensions.NoExtensionsDialog")

# Add state
if "var showNoExtensionsDialog" not in content:
    content = content.replace("var showSourceSheet by remember { mutableStateOf(false) }", "var showSourceSheet by remember { mutableStateOf(false) }\n    var showNoExtensionsDialog by remember { mutableStateOf(false) }")

# Update showSourceSheet = true
content = content.replace("showSourceSheet = true", """
                                        if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                            showNoExtensionsDialog = true
                                        } else {
                                            showSourceSheet = true
                                        }
""")

# Also need to add the NoExtensionsDialog component at the end of the screen logic
if "NoExtensionsDialog(" not in content:
    dialog_code = """
            if (showNoExtensionsDialog) {
                NoExtensionsDialog(
                    onDismiss = { showNoExtensionsDialog = false },
                    onGoToExtensions = { 
                        showNoExtensionsDialog = false
                        navController.navigate("extensions")
                    },
                    onRetry = {
                        if (ExtensionManager.installedExtensions.value.isNotEmpty()) {
                            showNoExtensionsDialog = false
                            showSourceSheet = true
                        }
                    }
                )
            }
"""
    # Just insert it before `if (showSourceSheet) {`
    content = content.replace("if (showSourceSheet) {", dialog_code.strip() + "\n            if (showSourceSheet) {")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)

