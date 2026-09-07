with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "if (!isCloudflare && document.readyState === 'complete') {" in line and new_lines and 'trimIndent' in new_lines[-1]:
        skip = True
    if skip and line.strip() == "}":
        skip = False
        continue
    if skip:
        continue
    new_lines.append(line)

# Now insert it at the correct place. Look for localPlay.click()
for i, line in enumerate(new_lines):
    if "if (localPlay) localPlay.click();" in line:
        insert_idx = i + 1
        break

fail_logic = """
                if (!isCloudflare && document.readyState === 'complete') {
                    window._failCount = (window._failCount || 0) + 1;
                    if (window._failCount >= 4) { 
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                    }
                }
"""

new_lines.insert(insert_idx, fail_logic)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.writelines(new_lines)
