import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_dialog = """Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {"""

new_dialog = """Dialog(
        onDismissRequest = {
            if (isLoading || isExtractingQualities) {
                showCancelConfirmDialog = true
            } else {
                onDismiss()
            }
        },
        properties = DialogProperties(
            usePlatformDefaultWidth = false,
            dismissOnClickOutside = false,
            dismissOnBackPress = true
        )
    ) {"""

if old_dialog in content:
    content = content.replace(old_dialog, new_dialog)
    print("Replaced old_dialog successfully.")
else:
    print("old_dialog not found!")

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

