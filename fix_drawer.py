import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

ext_item = """
                    NavigationDrawerItem(
                        icon = { Icon(Icons.Outlined.Settings, contentDescription = null, tint = MaterialTheme.colorScheme.onSurface) },
                        label = { Text("الإضافات", color = MaterialTheme.colorScheme.onSurface, fontSize = 16.sp) },
                        selected = currentRoute == Screen.Extensions.route,
                        colors = NavigationDrawerItemDefaults.colors(unselectedContainerColor = Color.Transparent),
                        onClick = {
                            scope.launch { drawerState.close() }
                            if (currentRoute != Screen.Extensions.route) {
                                navController.navigate(Screen.Extensions.route)
                            }
                        },
                        modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                    )
"""

if "label = { Text(\"الإضافات\"" not in content:
    content = content.replace("NavigationDrawerItem(\n                        icon = { Icon(Icons.Outlined.Settings", ext_item.lstrip() + "                    NavigationDrawerItem(\n                        icon = { Icon(Icons.Outlined.Settings")

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)

