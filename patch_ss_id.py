import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

old_func = """    fun getScriptForVideoExtractor(url: String): String {"""
new_func = """    fun getScriptForVideoExtractor(url: String, targetServerId: String? = null): String {"""
content = content.replace(old_func, new_func)

old_body = """                if (cf) { cf.click(); return; }
                
                var video = document.querySelector('video');"""
                
new_body = """                if (cf) { cf.click(); return; }
                
                var targetId = "${targetServerId ?: ""}";
                if (targetId && !window._serverClicked) {
                    var clicked = false;
                    // Site specific click logic based on ID format
                    if (targetId.includes('|')) {
                        var parts = targetId.split('|');
                        if (parts.length === 4) { // det.animerco.org
                            // Not easy to click, but we can try to find the option
                            var el = document.querySelector('a[data-post="'+parts[0]+'"][data-nume="'+parts[1]+'"]');
                            if (el) { el.click(); clicked = true; }
                        } else if (parts.length === 3) { // stardima.com
                            var el = document.querySelector('li[data-post="'+parts[0]+'"][data-nume="'+parts[1]+'"]');
                            if (el) { el.click(); clicked = true; }
                        } else if (parts.length === 2) { // topcinema.io
                            var el = document.querySelector('li[data-id="'+parts[0]+'"][data-server="'+parts[1]+'"]');
                            if (el) { el.click(); clicked = true; }
                        }
                    } else if (targetId.startsWith('server_')) { // z1.almeshkah.net
                        var el = document.getElementById(targetId);
                        if (el) { el.click(); clicked = true; }
                    } else { // witanime.you
                        var el = document.querySelector('a[data-server-id="'+targetId+'"]');
                        if (el) { el.click(); clicked = true; }
                    }
                    if (clicked) {
                        window._serverClicked = true;
                        return; // Wait for iframe to load
                    }
                }
                
                // Watch for new iframes after click
                if (window._serverClicked) {
                    var iframe = document.querySelector('div.player--iframe iframe, #iframe-container iframe, #Playerholder iframe, .videoWrapper iframe, .vp-embed iframe, #dooplay_player_response iframe');
                    if (iframe && iframe.src && iframe.src.startsWith('http') && iframe.src !== window._lastIframeSrc) {
                        window._lastIframeSrc = iframe.src;
                        if (typeof AndroidBridge !== 'undefined') {
                            AndroidBridge.sendIframeUrl(iframe.src);
                            clearInterval(intervalId);
                            return;
                        }
                    }
                }
                
                var video = document.querySelector('video');"""

content = content.replace(old_body, new_body)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)

