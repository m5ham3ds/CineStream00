import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

old_block = """                else if ("$siteName" === "arabseed.wine") {
                    var items = document.querySelectorAll('.servers__list li');
                    if(items.length === 0) items = document.querySelectorAll('[data-server]');
                    var currentIframe = document.querySelector('.player__iframe iframe');
                    var currentSrc = currentIframe ? currentIframe.getAttribute('src') : '';
                    
                    for (var i = 0; i < items.length; i++) {
                        var name = items[i].innerText.trim() || items[i].textContent.trim();if (!name) { var s = items[i].querySelector('span'); if (s) name = s.innerText.trim(); }if (!name) name = 'سيرفر ' + (i+1);
                        var link = items[i].getAttribute('data-player-url') || currentSrc;
                        if (!link) {
                            var meta = document.querySelector('meta[itemprop="contentURL"]');
                            if (meta) link = meta.getAttribute('content');
                        }
                        if(link) serverItems.push({ name: name, link: link });
                    }
                }"""

new_block = """                else if ("$siteName" === "arabseed.wine" || "$siteName" === "arabseed-tv.com") {
                    var items = document.querySelectorAll('.servers__list li, ul.d__flex.gap__20.flex__wrap.align__items__center.justify__content__center li, [data-server]');
                    var currentIframe = document.querySelector('.player__iframe iframe');
                    var currentSrc = currentIframe ? currentIframe.getAttribute('src') : '';
                    
                    for (var i = 0; i < items.length; i++) {
                        var name = items[i].innerText.trim() || items[i].textContent.trim();
                        if (!name) { var s = items[i].querySelector('span'); if (s) name = s.innerText.trim(); }
                        if (!name) name = 'سيرفر ' + (i+1);
                        var link = items[i].getAttribute('data-player-url');
                        if (!link) {
                            var dataServer = items[i].getAttribute('data-server');
                            if (dataServer) {
                                try { link = atob(dataServer); } catch(e) { link = dataServer; }
                            }
                        }
                        if (!link) link = currentSrc;
                        if (!link) {
                            var meta = document.querySelector('meta[itemprop="contentURL"]');
                            if (meta) link = meta.getAttribute('content');
                        }
                        if(link) serverItems.push({ name: name, link: link });
                    }
                }"""

content = content.replace(old_block, new_block)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)
print("Patched arabseed.")
