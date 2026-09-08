import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_cf = """                var isCloudflare = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, #challenge-form, .mark-as-human');
                if (cf) { cf.click(); return; }"""

new_cf = """                var isCloudflare = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
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
                    return;
                }"""
content = content.replace(old_cf, new_cf)

old_timeout = """                if (!isCloudflare && document.readyState === 'complete') {
                    window._failCount = (window._failCount || 0) + 1;
                    if (window._failCount >= 4) {"""
new_timeout = """                if (!isCloudflare && document.readyState === 'complete' && !window._serverClicked) {
                    window._failCount = (window._failCount || 0) + 1;
                    if (window._failCount >= 20) {"""
content = content.replace(old_timeout, new_timeout)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("Extractor patched!")
