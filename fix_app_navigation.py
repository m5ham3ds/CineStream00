with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

if "Screen.Extensions.route" not in content:
    content = content.replace("composable(Screen.Settings.route)", "composable(Screen.Extensions.route) { com.example.ui.screens.extensions.ExtensionsScreen(onBackClick = { navController.popBackStack() }) }\n                composable(Screen.Settings.route)")
    with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
        f.write(content)
