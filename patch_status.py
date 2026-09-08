import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Fix the CF reporting block in BOTH getScriptForSearch and getScriptForVideoExtractor
# First let's find the `if (isCloudflare || cf) {` block
old_cf_block = """                                if (isCloudflare || cf) {
                    if (!window._cfCssInjected) {
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
                        // Also try to find if it's nested
                        if (cf && cf.parentElement && cf.parentElement !== document.body) {
                            cf.parentElement.style.display = 'block';
                            cf.parentElement.style.position = 'absolute';
                            cf.parentElement.style.top = '50%';
                            cf.parentElement.style.left = '50%';
                            cf.parentElement.style.transform = 'translate(-50%, -50%)';
                        }
                    }
                    return;
                }"""

new_cf_block = """                                if (isCloudflare || cf) {
                    if (!window._cfCssInjected) {
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
                    }
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    return;
                } else {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }"""

content = content.replace(old_cf_block, new_cf_block)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("Added bridge status updates back.")
