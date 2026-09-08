import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Replace the Box modifier containing AndroidView
old_box = """                        key(retryTrigger) {
                            Box(modifier = if (bypassStatus == "CHECKING_CLOUDFLARE" || bypassStatus == "CLOUDFLARE") Modifier.fillMaxWidth().height(450.dp) else Modifier.size(1.dp).alpha(0f)) {"""

new_box = """                        key(retryTrigger) {
                            Box(
                                modifier = if (bypassStatus == "CLOUDFLARE") 
                                    Modifier.width(320.dp).height(150.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp))
                                else 
                                    Modifier.size(1.dp).alpha(0f),
                                contentAlignment = Alignment.Center
                            ) {"""

content = content.replace(old_box, new_box)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
