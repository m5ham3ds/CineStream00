import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

extractor_old = "HiddenVideoExtractor("

# Let's just find the first HiddenVideoExtractor which is inside `if (isLoading && !isFailed)`
idx = content.find("if (isLoading && !isFailed) {")
if idx != -1:
    h_idx = content.find("HiddenVideoExtractor(", idx)
    if h_idx != -1:
        # replace HiddenVideoExtractor( with key(retryTrigger) { HiddenVideoExtractor(
        new_content = content[:h_idx] + "key(retryTrigger) {\n                HiddenVideoExtractor(" + content[h_idx + len("HiddenVideoExtractor("):]
        # now we need to add the closing bracket after onServersFound = { ... } )
        close_paren_idx = new_content.find("onServersFound = { servers ->", h_idx)
        # find the end of this HiddenVideoExtractor call.
        # It ends after onServersFound block.
        if close_paren_idx != -1:
            end_block = new_content.find("            )", close_paren_idx)
            if end_block != -1:
                end_idx = end_block + len("            )")
                new_content = new_content[:end_idx] + "\n            }" + new_content[end_idx:]
                with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
                    f.write(new_content)
                print("Patched successfully")
            else:
                print("Could not find end of HiddenVideoExtractor call")
        else:
            print("Could not find onServersFound")
    else:
        print("Could not find HiddenVideoExtractor")
else:
    print("Could not find if (isLoading && !isFailed)")
