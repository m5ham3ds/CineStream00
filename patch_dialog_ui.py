import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Replace the Dialog opening block
old_dialog = """    Dialog(
        onDismissRequest = {
            if (isLoading) {
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

new_dialog = """    Dialog(
        onDismissRequest = {
            if (isLoading) {
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
    ) {
        // Handle Back Press manually to ensure it intercepts properly
        androidx.activity.compose.BackHandler {
            if (isLoading) {
                showCancelConfirmDialog = true
            } else {
                onDismiss()
            }
        }
        
        // Full screen box to catch outside clicks manually if properties fail
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.Black.copy(alpha = 0.6f))
                .clickable(
                    interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                    indication = null,
                    onClick = {
                        if (!isLoading) {
                            onDismiss()
                        }
                        // If isLoading, do nothing on outside click as per user request
                    }
                ),
            contentAlignment = Alignment.Center
        ) {"""

content = content.replace(old_dialog, new_dialog)

# I need to add an extra '}' at the end of the Dialog block for the new Box.
content = content.replace("            }\n        }\n    }\n}", "            }\n        }\n    }\n}\n}")

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("Patched dialog ui")
