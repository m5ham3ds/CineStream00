import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Replace the complicated CSS injection with a simple, robust overlay approach
old_css_regex = r"if \(!window\._cfCssInjected\) \{.*?(?=if \(typeof AndroidBridge !== 'undefined'\) AndroidBridge\.sendBypassStatus)"

new_css_logic = """if (!window._cfCssInjected) {
                        window._cfCssInjected = true;
                        var overlay = document.createElement('div');
                        overlay.id = 'aistudio-cf-overlay';
                        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background-color:#16161A;z-index:9999998;';
                        document.body.appendChild(overlay);
                        
                        if (cf) {
                            cf.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);z-index:9999999;';
                            if (cf.parentElement && cf.parentElement !== document.body) {
                                cf.parentElement.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);z-index:9999999;';
                            }
                        }
                    }
                    """

# Because regex with dotall can be tricky, let's use a simpler text replacement
# Find the exact block we injected last time
old_cf_block = """                    if (!window._cfCssInjected) {
                        window._cfCssInjected = true;
                        var style = document.createElement('style');
                        style.innerHTML = `
                            body, html { background-color: #16161A !important; }
                            body * { visibility: hidden !important; }
                            #challenge-stage, #challenge-stage *, .cf-turnstile-wrapper, .cf-turnstile-wrapper *, #challenge-form, #challenge-form * { visibility: visible !important; }
                            #challenge-stage, .cf-turnstile-wrapper, #challenge-form { 
                                position: fixed !important; 
                                top: 50% !important; 
                                left: 50% !important; 
                                transform: translate(-50%, -50%) !important; 
                                z-index: 999999 !important; 
                                margin: 0 !important;
                                padding: 0 !important;
                            }
                        `;
                        document.head.appendChild(style);
                        if (cf && cf.parentElement && cf.parentElement !== document.body) {
                            cf.parentElement.style.display = 'block';
                            cf.parentElement.style.position = 'absolute';
                            cf.parentElement.style.top = '50%';
                            cf.parentElement.style.left = '50%';
                            cf.parentElement.style.transform = 'translate(-50%, -50%)';
                        }
                    }"""

content = content.replace(old_cf_block, new_css_logic)

# Broaden the CF detection query selector
old_query = "var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, #challenge-form, .mark-as-human, #trk_jschal_js');"
new_query = "var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, #challenge-form, .mark-as-human, #trk_jschal_js, iframe[src*=\"challenges.cloudflare.com\"]');"
content = content.replace(old_query, new_query)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)

print("Overlay logic applied to SiteScripts.")
