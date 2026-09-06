package com.example.ui.screens.player

object SiteScripts {
    fun getScriptForSite(siteName: String, isMovie: Boolean, episode: Int): String {
        return """
        (function() {
            var intervalId = setInterval(function() {
                var isCloudflare = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
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
                    var videoElement = document.querySelector('video[src]');
                    if (videoElement) {
                        var videoUrl = videoElement.getAttribute('src');
                        if (videoUrl && (videoUrl.includes('.m3u8') || videoUrl.includes('.mp4'))) {
                            serverItems.push({ name: 'السيرفر الرئيسي', link: videoUrl });
                        }
                    } else {
                        // Click start button if on details page
                        var startBtn = document.querySelector('button, a[href*="/watch/"]');
                        if (startBtn && startBtn.innerText && startBtn.innerText.includes('ابدأ')) startBtn.click();
                    }
                } 
                else if ("$siteName" === "animeblkom.net") {
                    document.querySelectorAll('.servers .slider .item span.server a').forEach(function(a) {
                        var name = a.textContent.trim();
                        var link = a.getAttribute('data-src');
                        if (link) serverItems.push({ name: name, link: link });
                    });
                }
                else if ("$siteName" === "arabanime.net") {
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
                }
                else if ("$siteName" === "det.animerco.org") {
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
                else if ("$siteName" === "a.qfilm.tv") {
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
                }
                else if ("$siteName" === "arabseed.wine") {
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
                }
                else if ("$siteName" === "egybests.live") {
                    var items = document.querySelectorAll('#watch-servers-list li');
                    if (items.length === 0) items = document.querySelectorAll('.servList li');
                    for (var i = 0; i < items.length; i++) {
                        var name = items[i].innerText.trim() || items[i].textContent.trim() || ('سيرفر ' + (i+1));
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
                    document.querySelectorAll('#pm-servers ul.WatchList li').forEach(function(li) {
                        var name = li.querySelector('strong') ? li.querySelector('strong').textContent.trim() : 'سيرفر';
                        var embed = li.getAttribute('data-embed-url');
                        if (embed) serverItems.push({ name: name, link: embed });
                    });
                }
                else if ("$siteName" === "stardima.com" || "$siteName" === "watch.stardima.com") {
                    document.querySelectorAll('#playeroptionsul li.dooplay_player_option').forEach(function(el) {
                        var name = el.querySelector('.title') ? el.querySelector('.title').innerText.trim() : 'سيرفر';
                        var post = el.getAttribute('data-post');
                        var nume = el.getAttribute('data-nume');
                        var type = el.getAttribute('data-type');
                        if (post && nume) {
                            serverItems.push({ name: name, link: window.location.href, id: post + '|' + nume + '|' + type });
                        }
                    });
                }
                else if ("$siteName" === "e.cimalight.co") {
                    document.querySelectorAll('.embeding ul li').forEach(function(li) {
                        var name = li.textContent.trim();
                        var embed = li.getAttribute('data-embed');
                        if (embed) serverItems.push({ name: name, link: embed });
                    });
                }
                else if ("$siteName" === "topcinema.io") {
                    document.querySelectorAll('.watch--servers--list ul li.server--item').forEach(function(li) {
                        var name = li.querySelector('span') ? li.querySelector('span').innerText.trim() : 'سيرفر';
                        var id = li.getAttribute('data-id');
                        var server = li.getAttribute('data-server');
                        if (id && server) {
                            serverItems.push({ name: name, link: window.location.href, id: id + '|' + server });
                        }
                    });
                }
                else if ("$siteName" === "z1.almeshkah.net") {
                    document.querySelectorAll('ul.list_servers li').forEach(function(li) {
                        var name = li.querySelector('strong') ? li.querySelector('strong').innerText.trim() : 'سيرفر';
                        var embedHtml = li.getAttribute('data-embed');
                        if (embedHtml) {
                            var srcMatch = embedHtml.match(/src="([^"]+)"/);
                            if (srcMatch) serverItems.push({ name: name, link: srcMatch[1], id: li.id });
                        }
                    });
                }
                else if ("$siteName" === "uo.brstej.com") {
                    document.querySelectorAll('#WatchServers button.watchButton').forEach(function(btn, i) {
                        var name = btn.innerText.trim() || 'سيرفر ' + (i+1);
                        var link = btn.getAttribute('data-embed-url');
                        if(link) serverItems.push({ name: name, link: link });
                    });
                }
                else if ("$siteName" === "tv10.egydead.live") {
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
                }
                
                // Fallback for search and episodes matching
                if (serverItems.length === 0 && !loc.includes('watch')) {
                    if (loc.includes('?s=') || loc.includes('search') || loc.includes('query=')) {
                        var results = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a,  ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0');
                        if (results && results.length > 0) {
                            var targetResult = results[0];
                            if (!${isMovie}) {
                                var e = '${episode}';
                                for (var i=0; i<results.length; i++) {
                                    var txt = decodeURIComponent(results[i].href || "").toLowerCase() + " " + (results[i].innerText || results[i].title || results[i].getAttribute('title') || "").toLowerCase();
                                    if (txt.includes('حلقة ' + e) || txt.includes('حلقه ' + e) || txt.includes('-' + e + '-') || txt.includes('ep ' + e) || txt.includes('episode ' + e) || txt.includes(' ' + e + ' ')) {
                                        targetResult = results[i];
                                        break;
                                    }
                                }
                            }
                            clearInterval(intervalId);
                            window.location.href = targetResult.href;
                            return;
                        }
                    }
                    
                    if (!${isMovie}) {
                        var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a, ul#episodes-list-container li.episode-list-item a, .tabcontent ul a, div.anime-grid#episodesList a, .episodes-list-content a, ul.episodes-lists a, ul.episodes-links a, div.epnum a, div.hover a');
                        if (epLinks.length > 0) {
                            var targetEp = null;
                            var e = '${episode}';
                            for(var i=0; i<epLinks.length; i++) {
                                var text = epLinks[i].innerText || "";
                                if(text.trim() === e || text.includes(" " + e + " ") || text.includes("حلقة " + e) || text.includes("الحلقة " + e)) {
                                    targetEp = epLinks[i];
                                    break;
                                }
                            }
                            if(targetEp) {
                                clearInterval(intervalId);
                                var onclickAttr = targetEp.getAttribute('onclick');
                                if (onclickAttr && onclickAttr.includes('openEpisode(')) {
                                    var match = onclickAttr.match(/openEpisode\('([^']+)'\)/);
                                    if (match) {
                                        window.location.href = atob(match[1]);
                                        return;
                                    }
                                }
                                window.location.href = targetEp.href;
                                return;
                            }
                        }
                    }
                    
                    var watchNowBtn = document.querySelector('.watchNow button, .watchNow form button, .watch-btn, #watch-btn');
                    if (watchNowBtn) {
                        watchNowBtn.click();
                        return;
                    }
                }

                if (serverItems.length > 0) {
                    clearInterval(intervalId);
                    if (typeof AndroidBridge !== 'undefined') {
                        var finalItems = [];
                        for(var i=0; i<serverItems.length; i++){
                            var exists = false;
                            for(var j=0; j<finalItems.length; j++){ if(finalItems[j].name === serverItems[i].name) exists = true; }
                            if(!exists) finalItems.push(serverItems[i]);
                        }
                        AndroidBridge.sendServersV2(JSON.stringify(finalItems), window.location.href);
                    }
                    return;
                }
                
                var iframe = document.querySelector('iframe');
                if (iframe && iframe.src && !iframe.src.includes('cloudflare') && !iframe.src.includes('facebook')) {
                    clearInterval(intervalId);
                    if (typeof AndroidBridge !== 'undefined') {
                        AndroidBridge.sendServersV2(JSON.stringify([{name: "السيرفر الرئيسي", link: iframe.src}]), window.location.href);
                    }
                    return;
                }

                if (!isCloudflare && document.readyState === 'complete') {
                    var loc = window.location.href.toLowerCase();
                    var hasSearch = loc.includes('?s=') || loc.includes('?keywords=') || loc.includes('?search') || loc.includes('?query=');
                    
                    var isHome = false;
                    try {
                        var u = new URL(loc);
                        isHome = (u.pathname === '/' || u.pathname === '') && u.search === '';
                    } catch(e) {}
                    
                    var pageText = document.body ? document.body.innerText : "";
                    var notFound = pageText.includes("لا توجد نتائج") || pageText.includes("لم يتم العثور") || pageText.includes("لا يوجد") || pageText.includes("الصفحة غير موجودة") || pageText.includes("404") || pageText.includes("not found");

                    // If redirected to home page (lost search query) or explicitly no results found, fail instantly.
                    if (isHome || notFound) {
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                        return;
                    }

                    // Otherwise wait up to 4 intervals (6 seconds) before giving up
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
