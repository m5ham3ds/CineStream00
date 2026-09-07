package com.example.ui.screens.player

object SiteScripts {
    fun getScriptForSite(siteName: String, isMovie: Boolean, episode: Int, title: String): String {
        return """
        (function() {
            var intervalId = setInterval(function() {
                var isCloudflareTitle = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                var bodyText = document.body ? document.body.innerText : "";
                var isCloudflareText = bodyText.includes('Performing security verification') || bodyText.includes('protect against malicious bots') || bodyText.includes('verifies you are not a bot');
                var isCloudflare = isCloudflareTitle || isCloudflareText;
                var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                
                if (isCloudflare || cf) {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                    if (cf) cf.click();
                    return;
                } else {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                }
                
                var serverItems = [];
                var loc = window.location.href.toLowerCase();
                
                // --- SITE SPECIFIC LOGIC ---
                if ("$siteName" === "animeat.net") {
                    var videoElement = document.querySelector('video');
                    var videoUrl = null;
                    if (videoElement) {
                        videoUrl = videoElement.getAttribute('src');
                        if (!videoUrl || videoUrl === '') {
                            var sourceElement = videoElement.querySelector('source');
                            if (sourceElement) videoUrl = sourceElement.getAttribute('src');
                        }
                        if (videoUrl && (videoUrl.includes('.m3u8') || videoUrl.includes('.mp4') || videoUrl.includes('.mkv'))) {
                            serverItems.push({ name: 'السيرفر الرئيسي', link: videoUrl });
                        }
                    }
                    if (serverItems.length === 0) {
                        if (!window._animeatRetried) {
                            window._animeatRetried = true;
                            setTimeout(function() {
                                var retryVideo = document.querySelector('video');
                                if (retryVideo) {
                                    var retryUrl = retryVideo.getAttribute('src');
                                    if (!retryUrl || retryUrl === '') {
                                        var retrySource = retryVideo.querySelector('source');
                                        if (retrySource) retryUrl = retrySource.getAttribute('src');
                                    }
                                    if (retryUrl && (retryUrl.includes('.m3u8') || retryUrl.includes('.mp4'))) {
                                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendServersV2(JSON.stringify([{ name: 'السيرفر الرئيسي', link: retryUrl }]), window.location.href);
                                    }
                                }
                            }, 1500);
                        }
                        return;
                    }
                } 
                else if ("$siteName" === "animeblkom.net") {
                    var serverLinks = document.querySelectorAll('.servers .slider .item span.server a');
                    if (serverLinks && serverLinks.length > 0) {
                        serverLinks.forEach(function(a) {
                            var name = a.textContent.trim();
                            var link = a.getAttribute('data-src');
                            if (link && link.startsWith('http')) serverItems.push({ name: name, link: link });
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
                }
                else if ("$siteName" === "arabanime.net") {
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
                }
                else if ("$siteName" === "arabseed-tv.com" || "$siteName" === "arabseed.wine") {
                    var items = document.querySelectorAll('ul.servers__list li, .servers__list li, [data-server]');
                    if (items.length === 0) items = document.querySelectorAll('[data-server]');
                    
                    var currentIframe = document.querySelector('.player__iframe iframe');
                    var currentSrc = currentIframe ? currentIframe.getAttribute('src') : '';
                    
                    for (var i = 0; i < items.length; i++) {
                        var nameSpan = items[i].querySelector('span');
                        var name = nameSpan ? nameSpan.innerText.trim() : items[i].innerText.trim();
                        if (!name) name = 'سيرفر ' + (i + 1);
                        
                        var encodedLink = items[i].getAttribute('data-server');
                        var link = '';
                        if (encodedLink) {
                            try {
                                var decoded = atob(encodedLink);
                                if (decoded && !decoded.startsWith('http')) {
                                    try { decoded = atob(decoded); } catch(e2) {}
                                }
                                if (decoded && decoded.startsWith('http')) link = decoded;
                            } catch(e) {
                                link = currentSrc;
                            }
                        }
                        if (!link) {
                            link = items[i].getAttribute('data-player-url') || items[i].getAttribute('data-src') || items[i].getAttribute('data-link');
                        }
                        if (!link) {
                            if (items[i].classList.contains('active') && currentSrc) link = currentSrc;
                        }
                        if (!link) link = currentSrc;
                        
                        if (link && link.startsWith('http')) {
                            serverItems.push({ name: name, link: link });
                        }
                    }
                }
                else if ("$siteName" === "det.animerco.org") {
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
                }
                else if ("$siteName" === "e.cimalight.co") {
                    document.querySelectorAll('.embeding ul li, #sServer ul li').forEach(function(li) {
                        var name = li.textContent.trim().replace(/[^\w\s\u0600-\u06FF]/g, '').trim();
                        var embed = li.getAttribute('data-embed');
                        if (embed) serverItems.push({ name: name, link: embed });
                    });
                }
                else if ("$siteName" === "egybests.live") {
                    var items = document.querySelectorAll('#watch-servers-list li');
                    if (items.length === 0) items = document.querySelectorAll('.servList li');
                    var nameCount = {};
                    for (var i = 0; i < items.length; i++) {
                        var rawName = items[i].innerText.trim() || items[i].textContent.trim() || ('سيرفر');
                        var baseName = rawName.replace(/[^\w\s\u0600-\u06FF]/gi, '').trim();
                        if (!baseName) baseName = 'سيرفر';
                        if (!nameCount[baseName]) nameCount[baseName] = 0;
                        nameCount[baseName]++;
                        var name = baseName + (nameCount[baseName] > 1 ? ' ' + nameCount[baseName] : '');
                        
                        var onclick = items[i].getAttribute('onclick');
                        var url = '';
                        if (onclick) {
                            var match = onclick.match(/loadIframe\(this,\s*'([^']+)'\)/);
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
                }
                else if ("$siteName" === "laaroza.space") {
                    var serverLinks = document.querySelectorAll('#pm-servers ul.WatchList li');
                    if (serverLinks && serverLinks.length > 0) {
                        serverLinks.forEach(function(li) {
                            var name = li.querySelector('strong') ? li.querySelector('strong').textContent.trim() : 'سيرفر';
                            name = name.replace(/\s+/g, ' ').trim();
                            var embed = li.getAttribute('data-embed-url');
                            if (embed && embed.startsWith('http')) {
                                serverItems.push({ name: name, link: embed, active: li.classList.contains('active') });
                            }
                        });
                    }
                    if (serverItems.length === 0) {
                        var iframe = document.querySelector('#Playerholder iframe');
                        if (iframe && iframe.src && iframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الرئيسي', link: iframe.src, active: true });
                        }
                    }
                }
                else if ("$siteName" === "stardima.com" || "$siteName" === "watch.stardima.com") {
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
                }
                else if ("$siteName" === "topcinema.io") {
                    var serverLinks = document.querySelectorAll('.watch--servers--list ul li.server--item');
                    var currentIframe = document.querySelector('.player--iframe iframe');
                    var currentSrc = currentIframe ? currentIframe.src : '';
                    serverLinks.forEach(function(li) {
                        var name = li.querySelector('span') ? li.querySelector('span').textContent.trim() : 'سيرفر';
                        var postId = li.getAttribute('data-id');
                        var serverNum = li.getAttribute('data-server');
                        var isActive = li.classList.contains('active');
                        var link = isActive ? currentSrc : window.location.href;
                        serverItems.push({ name: name, link: link, id: postId, server: serverNum });
                    });
                }
                else if ("$siteName" === "tv10.egydead.live") {
                    var serverLinks = document.querySelectorAll('.mob-servers ul li');
                    if (serverLinks && serverLinks.length > 0) {
                        serverLinks.forEach(function(el, index) {
                            var nameEl = el.querySelector('p') || el.querySelector('span');
                            var name = nameEl ? nameEl.textContent.trim() : ('سيرفر ' + (index + 1));
                            name = name.replace(/\s+/g, ' ').trim();
                            var link = el.getAttribute('data-link') || el.getAttribute('data-src') || el.getAttribute('data-server');
                            if (link && link.startsWith('http')) serverItems.push({ name: name, link: link });
                        });
                    }
                    if (serverItems.length === 0) {
                        var iframe = document.querySelector('.mobIframe iframe');
                        if (iframe && iframe.src && iframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الرئيسي', link: iframe.src });
                        }
                    }
                }
                else if ("$siteName" === "uo.brstej.com") {
                    document.querySelectorAll('#WatchServers button.watchButton').forEach(function(btn) {
                        var name = btn.innerText.trim().replace(/[^\w\s\u0600-\u06FF]/g, '').trim();
                        var link = btn.getAttribute('data-embed-url');
                        var id = btn.getAttribute('data-embed-id');
                        if (link) serverItems.push({ name: name, link: link, id: id });
                    });
                }
                else if ("$siteName" === "vip.animeluxe.org") {
                    document.querySelectorAll('ul.server-list li a[data-url]').forEach(function(el) {
                        try {
                            var decodedUrl = atob(el.getAttribute('data-url'));
                            if (decodedUrl.startsWith('http')) {
                                var name = el.innerText.replace(/[^\w\s\u0600-\u06FF]/gi, '').trim();
                                if(!name) name = 'سيرفر';
                                serverItems.push({ name: name, link: decodedUrl });
                            }
                        } catch(e) {}
                    });
                }
                else if ("$siteName" === "w1.anime4up.rest") {
                    document.querySelectorAll('#episode-servers li').forEach(function(li) {
                        var name = li.querySelector('.watch-server-name') ? li.querySelector('.watch-server-name').textContent.trim() : 'سيرفر';
                        var watchUrl = li.getAttribute('data-watch');
                        if (watchUrl) serverItems.push({ name: name, link: watchUrl });
                    });
                }
                else if ("$siteName" === "witanime.you") {
                    document.querySelectorAll('#episode-servers li').forEach(function(li) {
                        var name = li.querySelector('.ser') ? li.querySelector('.ser').innerText.trim() : 'سيرفر';
                        var serverId = li.getAttribute('data-server-id');
                        if (serverId !== null) serverItems.push({ name: name, link: window.location.href, id: serverId });
                    });
                }
                else if ("$siteName" === "z1.almeshkah.net") {
                    document.querySelectorAll('ul.list_servers li').forEach(function(li) {
                        var name = li.querySelector('strong') ? li.querySelector('strong').innerText.trim() : 'سيرفر';
                        var embedHtml = li.getAttribute('data-embed');
                        if (embedHtml) {
                            var srcMatch = embedHtml.match(/src=["']([^"']+)["']/);
                            if (srcMatch) serverItems.push({ name: name, link: srcMatch[1], id: li.id });
                        }
                    });
                }
                else if ("$siteName" === "a.qfilm.tv") {
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
                            var name = btn.textContent.trim().replace(/[^\w\s\u0600-\u06FF]/gi, '').trim();
                            if (!name) name = 'سيرفر';
                            names.push(name);
                        });
                        for (var i = 0; i < serverArray.length && i < 20; i++) {
                            var iframeHtml = serverArray[i];
                            var srcMatch = iframeHtml.match(/src=["']([^"']+)["']/);
                            if (srcMatch && srcMatch[1].startsWith('http')) {
                                var name = (i < names.length && names[i]) ? names[i] : ('سيرفر ' + (i+1));
                                serverItems.push({ name: name, link: srcMatch[1] });
                            }
                        }
                    }
                    if (serverItems.length === 0) {
                        var currentIframe = document.querySelector('.embed_server iframe');
                        if (currentIframe && currentIframe.src && currentIframe.src.startsWith('http')) {
                            serverItems.push({ name: 'السيرفر الحالي', link: currentIframe.src });
                        }
                    }
                }
                
                // SEND SERVERS IF FOUND
                if (serverItems.length > 0) {
                    clearInterval(intervalId);
                    // Filter duplicates
                    var finalItems = [];
                    for(var i=0; i<serverItems.length; i++){
                        var exists = false;
                        for(var j=0; j<finalItems.length; j++){ if(finalItems[j].name === serverItems[i].name) exists = true; }
                        if(!exists) finalItems.push(serverItems[i]);
                    }
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendServersV2(JSON.stringify(finalItems), window.location.href);
                    return;
                }
                
                // --- SMART SEARCH RESULT MATCHER ---
                if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie'))) {
                    var searchTarget = "${title.lowercase().replace("'", "").replace("\"", "")}";
                    var results = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0, .GridItem a');
                    
                    if (results && results.length > 0) {
                        var targetResult = null;
                        for (var i = 0; i < results.length; i++) {
                            var linkText = (results[i].innerText || '') + " " + (results[i].getAttribute('title') || '');
                            linkText = linkText.toLowerCase().replace(/[^a-z0-9 ]/g, ''); 
                            var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '');
                            if (linkText.includes(normTarget)) { targetResult = results[i]; break; }
                        }
                        if (!targetResult) {
                            var words = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(' ').filter(function(w){ return w.length > 1; });
                            var bestMatchCount = 0;
                            var bestMatchElement = null;
                            for (var i = 0; i < results.length; i++) {
                                var linkText = (results[i].innerText || '') + " " + (results[i].getAttribute('title') || '');
                                linkText = linkText.toLowerCase().replace(/[^a-z0-9 ]/g, '');
                                var matchCount = 0;
                                for(var w = 0; w < words.length; w++) {
                                    if (linkText.includes(words[w])) matchCount++;
                                }
                                if (matchCount > bestMatchCount) {
                                    bestMatchCount = matchCount;
                                    bestMatchElement = results[i];
                                }
                            }
                            if (words.length > 0 && bestMatchCount >= Math.max(1, words.length - 1)) {
                                targetResult = bestMatchElement;
                            }
                        }
                        if (!targetResult && (loc.includes('?s=') || loc.includes('search') || loc.includes('query=') || loc.includes('keywords=') || loc.includes('?search_param='))) {
                            targetResult = results[0];
                        }
                        
                        if (targetResult) {
                            window.location.href = targetResult.href;
                            return;
                        }
                    } else if (loc.includes('searchq') || loc.includes('search') || loc.includes('?s=')) {
                        var input = document.querySelector('input[name="s"], input[name="query"], input[name="keywords"], input[name="search"]');
                        if (input && !input.value) {
                            input.value = "${title.replace("'", "'")}";
                            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                            if(btn) btn.click();
                            else if(input.form) input.form.submit();
                            return;
                        }
                    }
                }
                
                var iframe = document.querySelector('iframe');
                if (iframe && iframe.src && !iframe.src.includes('cloudflare') && !iframe.src.includes('facebook') && !iframe.src.includes('twitter')) {
                    clearInterval(intervalId);
                    if (typeof AndroidBridge !== 'undefined') {
                        AndroidBridge.sendServersV2(JSON.stringify([{name: "السيرفر الرئيسي", link: iframe.src}]), window.location.href);
                    }
                    return;
                }
                
                if (!isCloudflare && document.readyState === 'complete') {
                    window._failCount = (window._failCount || 0) + 1;
                    if (window._failCount >= 4) { 
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                    }
                }
            }, 1500);
        })();
        """.trimIndent()
    }

    fun getScriptForVideoExtractor(url: String, targetServerId: String? = null): String {
        return """
        (function() {
            var intervalId = setInterval(function() {
                var isCloudflare = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                if (cf) { cf.click(); return; }
                
                var targetId = "${targetServerId ?: ""}";
                if (targetId && !window._serverClicked) {
                    var clicked = false;
                    // Site specific click logic based on ID format
                    if (targetId.includes('|')) {
                        var parts = targetId.split('|');
                        if (parts.length === 4) { // det.animerco.org
                            var el = document.querySelector('a[data-post="'+parts[0]+'"][data-nume="'+parts[1]+'"]');
                            if (el) { el.click(); clicked = true; }
                        }
                    } else if (window.location.href.includes('topcinema')) {
                        var el = document.querySelector('li[data-id="'+targetId+'"]');
                        if (el) { el.click(); clicked = true; }
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
                if (window._serverClicked || !targetId) {
                    var iframe = document.querySelector('div.player--iframe iframe, #iframe-container iframe, #Playerholder iframe, .videoWrapper iframe, .vp-embed iframe, #dooplay_player_response iframe, .embed_server iframe, .embeding2 iframe, #video-player-container iframe');
                    if (iframe && iframe.src && iframe.src.startsWith('http') && iframe.src !== window._lastIframeSrc) {
                        window._lastIframeSrc = iframe.src;
                        if (typeof AndroidBridge !== 'undefined') {
                            AndroidBridge.sendIframeUrl(iframe.src);
                        }
                    }
                }
                
                var video = document.querySelector('video');
                if (video && video.src && !video.src.startsWith('blob:')) {
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendVideoUrl(video.src);
                    clearInterval(intervalId);
                    return;
                }
                
                var sources = document.querySelectorAll('video source');
                for (var i = 0; i < sources.length; i++) {
                    if (sources[i].src && !sources[i].src.startsWith('blob:')) {
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendVideoUrl(sources[i].src);
                        clearInterval(intervalId);
                        return;
                    }
                }
                
                var localPlay = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .fp-play, .play-icon, #play-video, .btn-play');
                if (localPlay) localPlay.click();
            }, 1000);
        })();
        """.trimIndent()
    }
}
