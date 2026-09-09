with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    content = f.read()

if "object Extensions" not in content:
    content = content.replace("object Search : Screen(", "object Extensions : Screen(\"extensions\", \"الإضافات\", Icons.Default.Settings)\n    object Search : Screen(")
    with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
        f.write(content)
