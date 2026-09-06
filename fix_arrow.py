with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

content = content.replace('androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack', 'androidx.compose.material.icons.Icons.Default.ArrowBack')

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
