import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Change the box modifier
old_box = "Box(modifier = if (isCloudflare) Modifier.fillMaxWidth().height(450.dp) else Modifier.size(1.dp).alpha(0f)) {"
new_box = "Box(modifier = if (bypassStatus == \"CHECKING_CLOUDFLARE\" || bypassStatus == \"CLOUDFLARE\") Modifier.fillMaxWidth().height(450.dp) else Modifier.size(1.dp).alpha(0f)) {"

if old_box in content:
    content = content.replace(old_box, new_box)
    print("WebView visibility fixed.")
else:
    print("Old box not found.")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
