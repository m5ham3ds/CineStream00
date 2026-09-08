import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Replace the ENTIRE cf block in BOTH places
# The block starts at `if (isCloudflare || cf) {` and ends at `return;`

old_pattern = r"""if \(isCloudflare \|\| cf\) \{.*?return;\s*\}"""

new_cf_logic = """if (isCloudflare || cf) {
                    if (!window._cfCssInjected) {
                        window._cfCssInjected = true;
                        var overlay = document.createElement('div');
                        overlay.id = 'aistudio-cf-overlay';
                        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background-color:#16161A;z-index:9999998;';
                        document.body.appendChild(overlay);
                        
                        if (cf) {
                            cf.style.position = 'fixed';
                            cf.style.top = '50%';
                            cf.style.left = '50%';
                            cf.style.transform = 'translate(-50%, -50%)';
                            cf.style.zIndex = '9999999';
                            cf.style.visibility = 'visible';
                            if (cf.parentElement && cf.parentElement !== document.body) {
                                cf.parentElement.style.position = 'fixed';
                                cf.parentElement.style.top = '50%';
                                cf.parentElement.style.left = '50%';
                                cf.parentElement.style.transform = 'translate(-50%, -50%)';
                                cf.parentElement.style.zIndex = '9999999';
                                cf.parentElement.style.visibility = 'visible';
                            }
                        }
                    }
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    return;
                }"""

content = re.sub(old_pattern, new_cf_logic, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("Regex replace applied.")
