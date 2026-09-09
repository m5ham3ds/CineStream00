import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace("onPersonClick = { personId -> navController.navigate(\"person/$personId\") },\n                        onPlay = {", "onPersonClick = { personId -> navController.navigate(\"person/$personId\") },\n                        onNavigateToExtensions = { navController.navigate(Screen.Extensions.route) },\n                        onPlay = {")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
