import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_inner = """        Box(
            modifier = Modifier
                .fillMaxWidth(0.95f)
                .wrapContentHeight()
                .clip(RoundedCornerShape(24.dp))
                .background(Color(0xFF16161A))
                .border(1.dp, Color(0x33FF1111), RoundedCornerShape(24.dp))
        ) {"""

new_inner = """        Box(
            modifier = Modifier
                .fillMaxWidth(0.95f)
                .wrapContentHeight()
                .clip(RoundedCornerShape(24.dp))
                .background(Color(0xFF16161A))
                .border(1.dp, Color(0x33FF1111), RoundedCornerShape(24.dp))
                .clickable(
                    interactionSource = remember { androidx.compose.foundation.interaction.MutableInteractionSource() },
                    indication = null,
                    onClick = {} // Consume clicks inside the dialog so they don't dismiss
                )
        ) {"""

content = content.replace(old_inner, new_inner)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("Patched inner box")
