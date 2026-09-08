import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# 1. Clean up the CF CSS
old_cf_block = """                        style.innerHTML = `
                            body * { visibility: hidden !important; color: transparent !important; background: transparent !important; }
                            body { background-color: #16161A !important; }
                            #challenge-stage *, .cf-turnstile-wrapper *, iframe { visibility: visible !important; color: inherit !important; background: inherit !important; }
                            #challenge-stage, .cf-turnstile-wrapper { position: fixed !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important; visibility: visible !important; z-index: 999999 !important; background: #16161A !important; }
                        `;"""

new_cf_block = """                        style.innerHTML = `
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
                        `;"""
content = content.replace(old_cf_block, new_cf_block) # Note: this will replace both instances if identical, but we'll check

# 2. Remove the normal CSS injection that broke text scraping
old_normal_block = """                } else {
                    if (!window._normalCssInjected) {
                        window._normalCssInjected = true;
                        var style = document.createElement('style');
                        style.innerHTML = `body { display: none !important; background-color: #16161A !important; }`;
                        document.head.appendChild(style);
                    }
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }"""
new_normal_block = """                } else {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }"""
content = content.replace(old_normal_block, new_normal_block)

# 3. Make innerText safer (use textContent to ignore CSS visibility issues if any remain)
content = content.replace("results[i].innerText", "(results[i].textContent || results[i].innerText || '')")

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("SiteScripts.kt patched!")

