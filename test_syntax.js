const script = `
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
                var siteName = "tv10.egydead.live";
                
                // --- SITE SPECIFIC LOGIC ---
                if (siteName === "animeat.net") {
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
                } 
                else if (siteName === "tv10.egydead.live") {
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
                
                if (serverItems.length > 0) {
                    var finalItems = serverItems;
                    clearInterval(intervalId);
                    if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendServersV2(JSON.stringify(finalItems), window.location.href);
                    return;
                }
                
                // --- SMART SEARCH RESULT MATCHER ---
                if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie'))) {
                    var searchTarget = "batman";
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
                            var link = targetResult.getAttribute('href');
                            if (link && link !== window.location.href) {
                                window.location.href = link;
                                return;
                            }
                        }
                    }
                }
                
                // If we are on an episode/movie page but no servers found yet
                var iframe = document.querySelector('iframe');
                if (iframe && iframe.src && iframe.src.startsWith('http') && !iframe.src.includes('youtube') && !iframe.src.includes('facebook') && !iframe.src.includes('twitter')) {
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
`;
try {
  new Function(script);
  console.log("Syntax is OK");
} catch (e) {
  console.error("Syntax Error:", e);
}
