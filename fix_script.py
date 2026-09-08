import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Replace return in Cloudflare block
old_return = """                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    return;
                } else {"""
new_return = """                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    // return; // We no longer return here so the script can keep checking for search results
                } else {"""
content = content.replace(old_return, new_return)

# Update fail conditions to avoid failing while Cloudflare element (cf) is present
old_fail_1 = """if (!isCloudflare && document.readyState === 'complete' && !window._isNavigating) {"""
new_fail_1 = """if (!(isCloudflare || cf) && document.readyState === 'complete' && !window._isNavigating) {"""
content = content.replace(old_fail_1, new_fail_1)

old_fail_2 = """if (!isCloudflare && document.readyState === 'complete' && !window._serverClicked) {"""
new_fail_2 = """if (!(isCloudflare || cf) && document.readyState === 'complete' && !window._serverClicked) {"""
content = content.replace(old_fail_2, new_fail_2)


with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
