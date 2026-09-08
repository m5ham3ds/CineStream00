import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# 1. Update the Cloudflare detection block to inject CSS and remove `cf.click()`
old_cf_block = """                var isCloudflare = isCloudflareTitle || isCloudflareText;
                var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, #challenge-form, .mark-as-human');
                
                if (isCloudflare || cf) {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    if (cf) cf.click();
                    return;
                } else {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }"""

new_cf_block = """                var isCloudflare = isCloudflareTitle || isCloudflareText;
                var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, #challenge-form, .mark-as-human, #trk_jschal_js');
                
                if (isCloudflare || cf) {
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
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    return;
                } else {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }"""

content = content.replace(old_cf_block, new_cf_block)

# 2. Fix navigation loops in search matcher
old_nav_1 = """                        if (targetResult) {
                            window.location.href = targetResult.href;
                            return;
                        }"""
new_nav_1 = """                        if (targetResult) {
                            if (!window._isNavigating) {
                                window._isNavigating = true;
                                window.location.href = targetResult.href;
                            }
                            return;
                        }"""
content = content.replace(old_nav_1, new_nav_1)

old_nav_2 = """                        if (input && !input.value) {
                            input.value = "${title.replace("'", "").replace("\"", "")}";
                            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                            if(btn) btn.click();
                            else if(input.form) input.form.submit();
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
content = content.replace(old_nav_2, new_nav_2)

old_nav_3 = """                    if (currentHref.includes('e.cimalight.co')) {
                        // cimalight watch.php -> click the embed or video to get iframe url
                        // handled by extractor below automatically
                    } else {
                        window.location.href = window.location.href.replace('watch.php', 'play.php');
                        return;
                    }"""
new_nav_3 = """                    if (currentHref.includes('e.cimalight.co')) {
                        // cimalight watch.php -> click the embed or video to get iframe url
                        // handled by extractor below automatically
                    } else {
                        if (!window._isNavigating) {
                            window._isNavigating = true;
                            window.location.href = window.location.href.replace('watch.php', 'play.php');
                        }
                        return;
                    }"""
content = content.replace(old_nav_3, new_nav_3)

# 3. Increase timeouts
old_timeout = """                if (!isCloudflare && document.readyState === 'complete') {
                    window._failCount = (window._failCount || 0) + 1;
                    var maxFails = (loc.includes('?s=') || loc.includes('search') || loc.includes('query=') || loc.includes('keywords=')) ? 2 : 4;
                    if (window._failCount >= maxFails) {"""
new_timeout = """                if (!isCloudflare && document.readyState === 'complete' && !window._isNavigating) {
                    window._failCount = (window._failCount || 0) + 1;
                    var maxFails = (loc.includes('?s=') || loc.includes('search') || loc.includes('query=') || loc.includes('keywords=')) ? 15 : 25; // wait ~20-35 seconds
                    if (window._failCount >= maxFails) {"""
content = content.replace(old_timeout, new_timeout)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("SiteScripts.kt patched successfully!")

