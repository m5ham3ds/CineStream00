import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# 1. Update the CSS for Cloudflare to perfectly hide everything except the challenge
old_css_block = """                        style.innerHTML = `
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

new_css_block = """                        style.innerHTML = `
                            body * { visibility: hidden !important; color: transparent !important; background: transparent !important; }
                            body { background-color: #16161A !important; }
                            #challenge-stage *, .cf-turnstile-wrapper *, iframe { visibility: visible !important; color: inherit !important; background: inherit !important; }
                            #challenge-stage, .cf-turnstile-wrapper { position: fixed !important; top: 50% !important; left: 50% !important; transform: translate(-50%, -50%) !important; visibility: visible !important; z-index: 999999 !important; background: #16161A !important; }
                        `;"""

content = content.replace(old_css_block, new_css_block)

# 2. Fix the navigation logic to ensure it clicks and doesn't get stuck
old_nav_1 = """                        if (targetResult) {
                            if (!window._isNavigating) {
                                window._isNavigating = true;
                                window.location.href = targetResult.href;
                            }
                            return;
                        }"""
new_nav_1 = """                        if (targetResult) {
                            if (!window._isNavigating) {
                                window._isNavigating = true;
                                targetResult.click();
                                setTimeout(function() { window.location.href = targetResult.href; }, 500);
                            }
                            return;
                        }"""
content = content.replace(old_nav_1, new_nav_1)

old_nav_2 = """                        if (input && !input.value) {
                            if (!window._isNavigating) {
                                window._isNavigating = true;
                                input.value = "${title.replace("'", "").replace("\"", "")}";
                                var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                                if(btn) btn.click();
                                else if(input.form) input.form.submit();
                            }
                            return;
                        }"""
new_nav_2 = """                        if (input && !input.value) {
                            if (!window._isNavigating) {
                                window._isNavigating = true;
                                input.value = "${title.replace("'", "").replace("\"", "")}";
                                var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                                if(btn) btn.click();
                                else if(input.form) input.form.submit();
                            }
                            return;
                        }"""

# 3. Add a check to hide WebView body if it's NOT Cloudflare, just in case sizing fails
old_normal_cf = """                } else {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }"""
new_normal_cf = """                } else {
                    if (!window._normalCssInjected) {
                        window._normalCssInjected = true;
                        var style = document.createElement('style');
                        style.innerHTML = `body { display: none !important; background-color: #16161A !important; }`;
                        document.head.appendChild(style);
                    }
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }"""
content = content.replace(old_normal_cf, new_normal_cf)


with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("SiteScripts patched!")
