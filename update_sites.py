import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

# 1. Update a.qfilm.tv
old_qfilm = """                else if ("$siteName" === "a.qfilm.tv") {
                    var serverArray = window.servers;
                    if (!serverArray && typeof servers !== 'undefined') serverArray = servers;
                    if (serverArray && Array.isArray(serverArray)) {
                        var buttons = document.querySelectorAll('.server-btn');
                        var names = [];
                        buttons.forEach(function(btn) { names.push(btn.innerText.trim()); });
                        for (var i = 0; i < serverArray.length; i++) {
                            var iframeHtml = serverArray[i];
                            var srcMatch = iframeHtml.match(/src=["']([^"']+)["']/);
                            if (srcMatch) {
                                var name = (i < names.length && names[i]) ? names[i] : ('سيرفر ' + (i+1));
                                serverItems.push({ name: name, link: srcMatch[1] });
                            }
                        }
                    }
                }"""
new_qfilm = """                else if ("$siteName" === "a.qfilm.tv") {
                    var serverArray = null;
                    if (typeof servers !== 'undefined' && Array.isArray(servers)) {
                        serverArray = servers;
                    } else if (typeof window.servers !== 'undefined' && Array.isArray(window.servers)) {
                        serverArray = window.servers;
                    }
                    if (serverArray && serverArray.length > 0) {
                        var buttons = document.querySelectorAll('.server-btn');
                        var names = [];
                        buttons.forEach(function(btn) {
                            var name = btn.textContent.trim();
                            name = name.replace(/[^\\w\\s\\u0600-\\u06FF]/gi, '').trim();
                            if (!name) name = 'سيرفر';
                            names.push(name);
                        });
                        for (var i = 0; i < serverArray.length && i < 20; i++) {
                            var iframeHtml = serverArray[i];
                            var parser = new DOMParser();
                            var doc = parser.parseFromString(iframeHtml, 'text/html');
                            var iframe = doc.querySelector('iframe');
                            var src = iframe ? iframe.getAttribute('src') : null;
                            if (!src) {
                                var srcMatch = iframeHtml.match(/src=["']([^"']+)["']/);
                                if (srcMatch) src = srcMatch[1];
                            }
                            if (src && src.startsWith('http')) {
                                var name = (i < names.length && names[i]) ? names[i] : ('سيرفر ' + (i+1));
                                serverItems.push({ name: name, link: src });
                            }
                        }
                    }
                    if (serverItems.length === 0) {
                        var currentIframe = document.querySelector('.embed_server iframe');
                        if (currentIframe && currentIframe.src && currentIframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الحالي', link: currentIframe.src });
                        }
                    }
                }"""
if old_qfilm in content:
    content = content.replace(old_qfilm, new_qfilm)


# 2. Update animeblkom.net
old_blkom = """                else if ("$siteName" === "animeblkom.net") {
                    document.querySelectorAll('.servers .slider .item span.server a').forEach(function(a) {
                        var name = a.textContent.trim();
                        var link = a.getAttribute('data-src');
                        if (link) serverItems.push({ name: name, link: link });
                    });
                }"""
new_blkom = """                else if ("$siteName" === "animeblkom.net") {
                    var serverLinks = document.querySelectorAll('.servers .slider .item span.server a');
                    if (serverLinks && serverLinks.length > 0) {
                        serverLinks.forEach(function(a) {
                            var name = a.textContent.trim();
                            var link = a.getAttribute('data-src');
                            if (link && link.startsWith('http')) {
                                serverItems.push({ name: name, link: link });
                            }
                        });
                    }
                    if (serverItems.length === 0) {
                        var currentIframe = document.querySelector('.video iframe');
                        if (currentIframe && currentIframe.src && currentIframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الحالي', link: currentIframe.src });
                        }
                    }
                    if (serverItems.length > 0 && serverItems.every(function(s) { return s.name === ''; })) {
                        var serverSpans = document.querySelectorAll('.servers .slider .item span.server');
                        serverSpans.forEach(function(span, index) {
                            if (index < serverItems.length) {
                                var name = span.className.replace('server', '').trim() || ('سيرفر ' + (index + 1));
                                serverItems[index].name = name;
                            }
                        });
                    }
                }"""
if old_blkom in content:
    content = content.replace(old_blkom, new_blkom)


# 3. Update arabanime.net
old_arabanime = """                else if ("$siteName" === "arabanime.net") {
                    var datawatchElement = document.getElementById('datawatch');
                    if (datawatchElement) {
                        try {
                            var jsonString = atob(datawatchElement.textContent.trim());
                            var data = JSON.parse(jsonString);
                            if (data.ep_info && data.ep_info.length > 0) {
                                var servers = data.ep_info[0].stream_servers || [];
                                servers.forEach(function(encodedUrl, index) {
                                    try {
                                        var decodedUrl = atob(encodedUrl);
                                        if (decodedUrl.startsWith('http')) serverItems.push({ name: 'سيرفر ' + (index + 1), link: decodedUrl });
                                    } catch(e) {}
                                });
                            }
                        } catch(e) {}
                    }
                    if (serverItems.length === 0) {
                        var serverInput = document.querySelector('form#form input[name="servers"]');
                        if (serverInput && serverInput.value) {
                            try { serverItems.push({ name: 'السيرفر الرئيسي', link: atob(serverInput.value) }); } catch(e) {}
                        }
                    }
                    if (serverItems.length === 0) {
                        var submitBtn = document.querySelector('form#form button[type="submit"]');
                        if (submitBtn) submitBtn.click();
                    }
                }"""
new_arabanime = """                else if ("$siteName" === "arabanime.net") {
                    var datawatchElement = document.getElementById('datawatch');
                    if (datawatchElement) {
                        try {
                            var jsonString = atob(datawatchElement.textContent.trim());
                            var data = JSON.parse(jsonString);
                            if (data.ep_info && data.ep_info.length > 0) {
                                var servers = data.ep_info[0].stream_servers || [];
                                var serverNames = data.ep_info[0].server_names || [];
                                servers.forEach(function(encodedUrl, index) {
                                    try {
                                        var decodedUrl = atob(encodedUrl);
                                        if (decodedUrl.startsWith('http')) {
                                            var name = (index < serverNames.length && serverNames[index]) ? serverNames[index] : ('سيرفر ' + (index + 1));
                                            serverItems.push({ name: name, link: decodedUrl });
                                        }
                                    } catch(e) {}
                                });
                            }
                        } catch(e) {}
                    }
                    if (serverItems.length === 0) {
                        var serverInput = document.querySelector('form#form input[name="servers"]');
                        if (serverInput && serverInput.value) {
                            try {
                                var decodedUrl = atob(serverInput.value);
                                if (decodedUrl.startsWith('http')) {
                                    serverItems.push({ name: 'السيرفر الرئيسي', link: decodedUrl });
                                }
                            } catch(e) {}
                        }
                    }
                    if (serverItems.length === 0) {
                        var submitBtn = document.querySelector('form#form button[type="submit"]');
                        if (submitBtn) submitBtn.click();
                    }
                }"""
if old_arabanime in content:
    content = content.replace(old_arabanime, new_arabanime)

# 4. Update arabseed.wine / arabseed-tv.com
old_arabseed = """                else if ("$siteName" === "arabseed.wine") {
                    var items = document.querySelectorAll('.servers__list li');
                    if(items.length === 0) items = document.querySelectorAll('[data-server]');
                    var currentIframe = document.querySelector('.player__iframe iframe');
                    var currentSrc = currentIframe ? currentIframe.getAttribute('src') : '';
                    
                    for (var i = 0; i < items.length; i++) {
                        var name = items[i].innerText.trim() || items[i].textContent.trim();
                        if (!name) { var s = items[i].querySelector('span'); if (s) name = s.innerText.trim(); }
                        if (!name) name = 'سيرفر ' + (i+1);

                        var link = items[i].getAttribute('data-player-url') || currentSrc;
                        if (!link) {
                            var meta = document.querySelector('meta[itemprop="contentURL"]');
                            if (meta) link = meta.getAttribute('content');
                        }
                        if(link) serverItems.push({ name: name, link: link });
                    }
                }"""
new_arabseed = """                else if ("$siteName" === "arabseed.wine" || "$siteName" === "arabseed-tv.com") {
                    var items = document.querySelectorAll('ul.servers__list li, .servers__list li, [data-server]');
                    if (items.length === 0) {
                        items = document.querySelectorAll('[data-server]');
                    }
                    
                    var currentIframe = document.querySelector('.player__iframe iframe');
                    var currentSrc = currentIframe ? currentIframe.getAttribute('src') : '';
                    
                    for (var i = 0; i < items.length; i++) {
                        var name = items[i].querySelector('span') ? items[i].querySelector('span').innerText.trim() : '';
                        if (!name) {
                            name = items[i].innerText.trim() || items[i].textContent.trim();
                        }
                        if (!name) name = 'سيرفر ' + (i + 1);
                        
                        var encodedLink = items[i].getAttribute('data-server');
                        var link = '';
                        
                        if (encodedLink) {
                            try {
                                var decoded = atob(encodedLink);
                                if (decoded && !decoded.startsWith('http')) {
                                    try {
                                        decoded = atob(decoded);
                                    } catch(e2) {}
                                }
                                if (decoded && decoded.startsWith('http')) {
                                    link = decoded;
                                }
                            } catch(e) {
                                link = currentSrc;
                            }
                        }
                        
                        if (!link) link = items[i].getAttribute('data-player-url') || items[i].getAttribute('data-src') || items[i].getAttribute('data-link');
                        if (!link) {
                            if (items[i].classList.contains('active') && currentSrc) link = currentSrc;
                        }
                        if (!link) link = currentSrc;
                        
                        if (link && link.startsWith('http')) {
                            serverItems.push({ name: name, link: link });
                        }
                    }
                    if (serverItems.length === 0 && currentSrc) {
                        serverItems.push({ name: 'السيرفر الرئيسي', link: currentSrc });
                    }
                }"""
if old_arabseed in content:
    content = content.replace(old_arabseed, new_arabseed)


# 5. Update det.animerco.org
old_det = """                else if ("$siteName" === "det.animerco.org") {
                    document.querySelectorAll('ul.server-list li a.option').forEach(function(el) {
                        var name = el.querySelector('.server') ? el.querySelector('.server').innerText.trim() : 'سيرفر';
                        var post = el.getAttribute('data-post');
                        var nume = el.getAttribute('data-nume');
                        var nonce = el.getAttribute('data-nonce');
                        var type = el.getAttribute('data-type');
                        if (post && nume && nonce) {
                            serverItems.push({ name: name, link: window.location.href, id: post + '|' + nume + '|' + nonce + '|' + type });
                        }
                    });
                }"""
new_det = """                else if ("$siteName" === "det.animerco.org") {
                    var serverLinks = document.querySelectorAll('ul.server-list li a.option');
                    if (serverLinks && serverLinks.length > 0) {
                        var activeIframe = document.querySelector('#player iframe');
                        var activeSrc = activeIframe ? activeIframe.src : '';
                        
                        serverLinks.forEach(function(el, index) {
                            var name = el.querySelector('.server') ? el.querySelector('.server').innerText.trim() : ('سيرفر ' + (index + 1));
                            var post = el.getAttribute('data-post');
                            var nume = el.getAttribute('data-nume');
                            var nonce = el.getAttribute('data-nonce');
                            var type = el.getAttribute('data-type');
                            
                            if (post && nume && nonce) {
                                var link = el.classList.contains('active') ? activeSrc : window.location.href;
                                serverItems.push({
                                    name: name,
                                    link: link,
                                    id: post + '|' + nume + '|' + nonce + '|' + type
                                });
                            }
                        });
                    }
                    if (serverItems.length === 0) {
                        var iframe = document.querySelector('#player iframe');
                        if (iframe && iframe.src && iframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الرئيسي', link: iframe.src });
                        }
                    }
                }"""
if old_det in content:
    content = content.replace(old_det, new_det)

# 6. Update egybests.live
old_egybest = """                else if ("$siteName" === "egybests.live") {
                    var items = document.querySelectorAll('#watch-servers-list li');
                    if (items.length === 0) items = document.querySelectorAll('.servList li');
                    for (var i = 0; i < items.length; i++) {
                        var name = items[i].innerText.trim() || items[i].textContent.trim() || ('سيرفر ' + (i+1));
                        var onclick = items[i].getAttribute('onclick');
                        var url = '';
                        if (onclick) {
                            var match = onclick.match(/loadIframe\\(this,\\s*'([^']+)'\\)/);
                            if (match) url = match[1];
                        }
                        if (!url) url = items[i].getAttribute('data-link') || items[i].getAttribute('data-url') || '';
                        if (url) {
                            try {
                                var urlObj = new URL(url);
                                var encoded = urlObj.searchParams.get('url');
                                if (encoded) {
                                    var decoded = atob(decodeURIComponent(encoded));
                                    if (decoded.startsWith('http')) url = decoded;
                                }
                            } catch(e) {}
                            serverItems.push({ name: name, link: url });
                        }
                    }
                }"""
new_egybest = """                else if ("$siteName" === "egybests.live") {
                    var items = document.querySelectorAll('#watch-servers-list li');
                    if (items.length === 0) items = document.querySelectorAll('.servList li');
                    
                    var nameCount = {};
                    for (var i = 0; i < items.length; i++) {
                        var rawName = items[i].innerText.trim() || items[i].textContent.trim() || ('سيرفر');
                        var baseName = rawName.replace(/[^\\w\\s\\u0600-\\u06FF]/gi, '').trim();
                        if (!baseName) baseName = 'سيرفر';
                        
                        if (!nameCount[baseName]) nameCount[baseName] = 0;
                        nameCount[baseName]++;
                        var name = baseName + (nameCount[baseName] > 1 ? ' ' + nameCount[baseName] : '');
                        
                        var onclick = items[i].getAttribute('onclick');
                        var url = '';
                        if (onclick) {
                            var match = onclick.match(/loadIframe\\(this,\\s*'([^']+)'\\)/);
                            if (match) url = match[1];
                        }
                        if (!url) url = items[i].getAttribute('data-link') || items[i].getAttribute('data-url') || '';
                        if (url) {
                            try {
                                var urlObj = new URL(url);
                                var encoded = urlObj.searchParams.get('url');
                                if (encoded) {
                                    var decoded = atob(decodeURIComponent(encoded));
                                    if (decoded.startsWith('http')) url = decoded;
                                }
                            } catch(e) {}
                            serverItems.push({ name: name, link: url });
                        }
                    }
                }"""
if old_egybest in content:
    content = content.replace(old_egybest, new_egybest)

# 7. Update laaroza.space
old_laaroza = """                else if ("$siteName" === "laaroza.space") {
                    document.querySelectorAll('#pm-servers ul.WatchList li').forEach(function(li) {
                        var name = li.querySelector('strong') ? li.querySelector('strong').textContent.trim() : 'سيرفر';
                        var embed = li.getAttribute('data-embed-url');
                        if (embed) serverItems.push({ name: name, link: embed });
                    });
                }"""
new_laaroza = """                else if ("$siteName" === "laaroza.space") {
                    var serverLinks = document.querySelectorAll('#pm-servers ul.WatchList li');
                    if (serverLinks && serverLinks.length > 0) {
                        serverLinks.forEach(function(li) {
                            var name = li.querySelector('strong') ? li.querySelector('strong').textContent.trim() : 'سيرفر';
                            name = name.replace(/\\s+/g, ' ').trim();
                            var embed = li.getAttribute('data-embed-url');
                            if (embed && embed.startsWith('http')) {
                                serverItems.push({ name: name, link: embed });
                            }
                        });
                    }
                    if (serverItems.length === 0) {
                        var iframe = document.querySelector('#Playerholder iframe');
                        if (iframe && iframe.src && iframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الرئيسي', link: iframe.src });
                        }
                    }
                }"""
if old_laaroza in content:
    content = content.replace(old_laaroza, new_laaroza)

# 8. Update stardima.com
old_stardima = """                else if ("$siteName" === "stardima.com" || "$siteName" === "watch.stardima.com") {
                    document.querySelectorAll('#pm-servers ul.WatchList li').forEach(function(li) {
                        var name = li.querySelector('strong') ? li.querySelector('strong').textContent.trim() : 'سيرفر';
                        var embed = li.getAttribute('data-embed-url');
                        if (embed) serverItems.push({ name: name, link: embed });
                    });
                }"""
new_stardima = """                else if ("$siteName" === "stardima.com" || "$siteName" === "watch.stardima.com") {
                    var iframe = document.querySelector('#video-player-container iframe');
                    if (iframe && iframe.src && iframe.src.startsWith('http')) {
                        serverItems.push({ name: 'المشغل الحالي', link: iframe.src });
                    }
                    var episodeLinks = document.querySelectorAll('#episodes-list-container li.episode-list-item a');
                    if (episodeLinks && episodeLinks.length > 0) {
                        episodeLinks.forEach(function(a, index) {
                            var name = a.textContent.trim();
                            if (!name) name = 'حلقة ' + (index + 1);
                            var href = a.getAttribute('href');
                            if (href && href.includes('/play/')) {
                                var fullUrl = window.location.origin + href;
                                serverItems.push({ name: name, link: fullUrl });
                            }
                        });
                    }
                }"""
if old_stardima in content:
    content = content.replace(old_stardima, new_stardima)

# 9. Update topcinema.io
old_topcinema = """                else if ("$siteName" === "topcinema.io") {
                    document.querySelectorAll('.watch--servers--list ul li.server--item').forEach(function(li) {
                        var name = li.querySelector('span') ? li.querySelector('span').textContent.trim() : 'سيرفر';
                        var link = li.getAttribute('data-player-url');
                        if (!link) {
                            link = li.getAttribute('data-link');
                        }
                        if (!link) {
                            var iframe = document.querySelector('.player--iframe iframe');
                            link = iframe ? iframe.getAttribute('src') : '';
                        }
                        if (link && link.startsWith('http')) {
                            serverItems.push({ name: name, link: link });
                        }
                    });
                }"""
new_topcinema = """                else if ("$siteName" === "topcinema.io") {
                    var serverLinks = document.querySelectorAll('.watch--servers--list ul li.server--item');
                    var currentIframe = document.querySelector('.player--iframe iframe');
                    var currentSrc = currentIframe ? currentIframe.src : '';
                    
                    serverLinks.forEach(function(li) {
                        var name = li.querySelector('span') ? li.querySelector('span').textContent.trim() : 'سيرفر';
                        var postId = li.getAttribute('data-id');
                        var serverNum = li.getAttribute('data-server');
                        var isActive = li.classList.contains('active');
                        var link = isActive ? currentSrc : '';
                        
                        serverItems.push({
                            name: name,
                            link: link || currentSrc,
                            id: postId + '|' + serverNum
                        });
                    });
                }"""
if old_topcinema in content:
    content = content.replace(old_topcinema, new_topcinema)

# 10. Update tv10.egydead.live
old_egydead = """                else if ("$siteName" === "tv10.egydead.live") {
                    // Fallback using data-link or data-server
                    var items = document.querySelectorAll('ul.WatchServers li.server--item, ul.servers__list li, .servers-list li, .serversList li, ul.servers li, .mob-servers ul li');
                    items.forEach(function(el, i) {
                        var link = el.getAttribute('data-link') || el.getAttribute('data-watch') || el.getAttribute('data-src') || el.getAttribute('data-server');
                        if(!link && el.hasAttribute('onclick')) {
                            var m = el.getAttribute('onclick').match(/loadIframe\\(this,\\s*'([^']+)'\\)/);
                            if(m) link = m[1];
                        }
                        if(!link && el.href && el.href.includes('http') && !el.href.includes(window.location.host)) {
                            link = el.href;
                        }
                        var name = el.innerText.trim() || el.textContent.trim();
                        if (!name) { var s = el.querySelector('span'); if (s) name = s.innerText.trim(); }
                        if (!name) name = 'سيرفر ' + (i+1);
                        if(link) serverItems.push({ name: name, link: link });
                    });
                }"""
new_egydead = """                else if ("$siteName" === "tv10.egydead.live") {
                    var serverLinks = document.querySelectorAll('.mob-servers ul li');
                    if (serverLinks && serverLinks.length > 0) {
                        serverLinks.forEach(function(el, index) {
                            var nameEl = el.querySelector('p');
                            if (!nameEl) nameEl = el.querySelector('span');
                            var name = nameEl ? nameEl.textContent.trim() : ('سيرفر ' + (index + 1));
                            name = name.replace(/\\s+/g, ' ').trim();
                            
                            var link = el.getAttribute('data-link') || el.getAttribute('data-src') || el.getAttribute('data-server');
                            if (link && link.startsWith('http')) {
                                serverItems.push({ name: name, link: link });
                            }
                        });
                    }
                    if (serverItems.length === 0) {
                        var iframe = document.querySelector('.mobIframe iframe');
                        if (iframe && iframe.src && iframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الرئيسي', link: iframe.src });
                        }
                    }
                }"""
if old_egydead in content:
    content = content.replace(old_egydead, new_egydead)

# 11. Update uo.brstej.com
old_brstej = """                else if ("$siteName" === "uo.brstej.com") {
                    // Fallback using data-link or data-server
                    var items = document.querySelectorAll('ul.WatchServers li.server--item, ul.servers__list li, .servers-list li, .serversList li, ul.servers li, .mob-servers ul li');
                    items.forEach(function(el, i) {
                        var link = el.getAttribute('data-link') || el.getAttribute('data-watch') || el.getAttribute('data-src') || el.getAttribute('data-server');
                        if(!link && el.hasAttribute('onclick')) {
                            var m = el.getAttribute('onclick').match(/loadIframe\\(this,\\s*'([^']+)'\\)/);
                            if(m) link = m[1];
                        }
                        if(!link && el.href && el.href.includes('http') && !el.href.includes(window.location.host)) {
                            link = el.href;
                        }
                        var name = el.innerText.trim() || el.textContent.trim();
                        if (!name) { var s = el.querySelector('span'); if (s) name = s.innerText.trim(); }
                        if (!name) name = 'سيرفر ' + (i+1);
                        if(link) serverItems.push({ name: name, link: link });
                    });
                }"""
new_brstej = """                else if ("$siteName" === "uo.brstej.com") {
                    document.querySelectorAll('#WatchServers button.watchButton').forEach(function(btn) {
                        var name = btn.innerText.trim();
                        name = name.replace(/[^\\w\\s\\u0600-\\u06FF]/g, '').trim();
                        var link = btn.getAttribute('data-embed-url');
                        var id = btn.getAttribute('data-embed-id');
                        if (link) {
                            serverItems.push({ name: name, link: link, id: id });
                        }
                    });
                }"""
if old_brstej in content:
    content = content.replace(old_brstej, new_brstej)


with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)

print("Updated 11 sites in SiteScripts.kt")
