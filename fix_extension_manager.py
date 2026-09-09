with open("app/src/main/java/com/example/extensions/ExtensionManager.kt", "r") as f:
    content = f.read()

content = content.replace("private lateinit val prefs", "private lateinit var prefs")

with open("app/src/main/java/com/example/extensions/ExtensionManager.kt", "w") as f:
    f.write(content)
