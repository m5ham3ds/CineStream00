import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

old_code = """    if (showDownloadSheet) {
        DownloadQualitySheet(
            onDismiss = { showDownloadSheet = false },
            onQualitySelected = { quality ->"""

new_code = """    if (showDownloadSheet) {
        DownloadQualitySheet(
            qualities = availableVideoQualities.filter { it != "Auto" }.ifEmpty { listOf("Default") },
            onDismiss = { showDownloadSheet = false },
            onQualitySelected = { quality ->"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
