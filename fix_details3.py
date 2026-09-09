import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace(
"""                    onGoToExtensions = { 
                        showNoExtensionsDialog = false
                        onNavigateToExtensions()
                    },""",
"""                    onGoToExtensions = { 
                        onNavigateToExtensions()
                    },""")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
