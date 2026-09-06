import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

idx = content.find("if (isLoading && !isFailed) {")
if idx != -1:
    h_idx = content.find("AndroidView(", idx)
    if h_idx != -1:
        # replace AndroidView( with key(retryTrigger) { AndroidView(
        new_content = content[:h_idx] + "key(retryTrigger) {\n            AndroidView(" + content[h_idx + len("AndroidView("):]
        # find the end of this AndroidView block...
        # Wait, the AndroidView ends at line 301. It has an update = { ... }. Let's find update = { block end.
        up_idx = new_content.find("update = { webView ->", h_idx)
        if up_idx != -1:
            end_update = new_content.find("            }\n        )", up_idx)
            if end_update != -1:
                end_idx = end_update + len("            }\n        )")
                new_content = new_content[:end_idx] + "\n        }" + new_content[end_idx:]
                with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
                    f.write(new_content)
                print("Patched successfully")
            else:
                print("Could not find end of update")
        else:
            print("Could not find update =")
    else:
        print("Could not find AndroidView")
else:
    print("Could not find if (isLoading && !isFailed)")
