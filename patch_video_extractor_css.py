import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Make sure CSS injection for Cloudflare in extractor is identical to search
old_ext_cf = """                if (isCloudflare || cf) {
                    if (!window._cfCssInjected) {
                        window._cfCssInjected = true;
                        var style = document.createElement('style');
                        style.innerHTML = `
                            body { background-color: #16161A !important; }
                            body > * { display: none !important; }
                            body > #challenge-form, 
                            body > #challenge-stage, 
                            body > .cf-turnstile-wrapper,
                            body > iframe,
                            body > #trk_jschal_js { 
                                display: block !important; 
                                position: absolute !important; 
                                top: 50% !important; 
                                left: 50% !important; 
                                transform: translate(-50%, -50%) !important; 
                                z-index: 999999 !important;
                                margin: 0 !important;
                            }
                        `;"""

new_ext_cf = """                if (isCloudflare || cf) {
                    if (!window._cfCssInjected) {
                        window._cfCssInjected = true;
                        var style = document.createElement('style');
                        style.innerHTML = `
                            body * { visibility: hidden !important; color: transparent !important; background: transparent !important; }
                            body { background-color: #16161A !important; }
                            #challenge-stage *, .cf-turnstile-wrapper *, iframe { visibility: visible !important; color: inherit !important; background: inherit !important; }
                            #challenge-stage, .cf-turnstile-wrapper { position: fixed !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important; visibility: visible !important; z-index: 999999 !important; background: #16161A !important; }
                        `;"""

content = content.replace(old_ext_cf, new_ext_cf)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("Extractor CSS patched!")
