import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Replace any occurrence of the specific JS block without the AndroidBridge lines
old_pattern = r"""(\s*if \(cf && cf\.parentElement && cf\.parentElement !== document\.body\) \{\s*cf\.parentElement\.style\.display = 'block';\s*cf\.parentElement\.style\.position = 'absolute';\s*cf\.parentElement\.style\.top = '50%';\s*cf\.parentElement\.style\.left = '50%';\s*cf\.parentElement\.style\.transform = 'translate\(-50%, -50%\)';\s*\})\s*\}\s*return;"""

# Replace it with the version that includes the bridge updates
new_pattern = r"""\1
                    }
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    return;
                } else {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");"""

content_new = re.sub(old_pattern, new_pattern, content)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content_new)

if content != content_new:
    print("Patched both occurrences successfully.")
else:
    print("No changes made. Might already be patched.")
