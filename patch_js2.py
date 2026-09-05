import re
import json

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

start_idx = content.find("var intervalId = setInterval(function() {")
end_idx = content.find("})();", start_idx)

if start_idx != -1 and end_idx != -1:
    old_js = content[start_idx:end_idx]
    
    new_js = """var intervalId = setInterval(function() {
                                        // Bypass Cloudflare
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        var isJustAMoment = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                                        var isCloudflare = cf || isJustAMoment;
                                        
                                        if (isCloudflare) {
                                            if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                                            if (cf) cf.click();
                                            return;
                                        } else {
                                            if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                                        }

                                        // 1. Search Results -> Click item
                                        if (loc.includes('?s=') || loc.includes('search') || loc.includes('query=')) {
                                            var results = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a,  ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0');
                                            if (results && results.length > 0) {
                                                clearInterval(intervalId);
                                                var targetResult = results[0];
                                                if (!isMovie) {
                                                    var e = epNum.toString();
                                                    for (var i=0; i<results.length; i++) {
                                                        var txt = decodeURIComponent(results[i].href || "").toLowerCase() + " " + (results[i].innerText || results[i].title || results[i].getAttribute('title') || "").toLowerCase();
                                                        if (txt.includes('حلقة ' + e) || txt.includes('حلقه ' + e) || txt.includes('-' + e + '-') || txt.includes('ep ' + e) || txt.includes('episode ' + e) || txt.includes(' ' + e + ' ')) {
                                                            targetResult = results[i];
                                                            break;
                                                        }
                                                    }
                                                }
                                                window.location.href = targetResult.href;
                                                return;
                                            }
                                        }
                                        
                                        // 2. Series Page -> Click Season/Episode
                                        var iframes = document.querySelectorAll('iframe');
                                        var hasIframe = false;
                                        for(var i=0; i<iframes.length; i++) {
                                            if(iframes[i].src && !iframes[i].src.includes('cloudflare') && !iframes[i].src.includes('facebook') && !iframes[i].src.includes('twitter')) {
                                                hasIframe = true; break;
                                            }
                                        }
                                        var videoTags = document.querySelectorAll('video');
                                        var hasVideo = videoTags.length > 0;
                                        
                                        var serverItems = [];
                                        
                                        // (A) Standard data-link, data-watch, data-src servers
                                        var linkElements = document.querySelectorAll('[data-link], [data-watch], [data-src], ul#episode-servers li a.server-link');
                                        for(var i=0; i<linkElements.length; i++) {
                                            var el = linkElements[i];
                                            var link = el.getAttribute('data-link') || el.getAttribute('data-watch') || el.getAttribute('data-src');
                                            if(!link && el.hasAttribute('onclick')) {
                                                // Try to extract from onclick="loadIframe(this, 'url')"
                                                var onclickStr = el.getAttribute('onclick');
                                                var m = onclickStr.match(/loadIframe\\(this,\\s*'([^']+)'\\)/);
                                                if(m) link = m[1];
                                            }
                                            if(!link && el.href && el.href.includes('http') && !el.href.includes(window.location.host)) {
                                                link = el.href;
                                            }
                                            var name = el.innerText.trim() || el.getAttribute('title') || 'سيرفر ' + (i+1);
                                            if (link && link.startsWith('http') && !link.includes('facebook') && !link.includes('twitter')) {
                                                serverItems.push({ name: name, link: link });
                                            }
                                        }
                                        
                                        // (B) qfilm (Array of iframes in 'servers' variable)
                                        if (typeof servers !== 'undefined' && Array.isArray(servers)) {
                                            var btnNames = document.querySelectorAll('button.server-btn');
                                            for(var i=0; i<servers.length; i++) {
                                                var html = servers[i];
                                                var srcMatch = html.match(/src=["']([^"']+)["']/);
                                                if (srcMatch) {
                                                    var name = btnNames[i] ? btnNames[i].innerText.trim() : 'سيرفر ' + (i+1);
                                                    serverItems.push({ name: name, link: srcMatch[1] });
                                                }
                                            }
                                        }
                                        
                                        // (C) topcinema & arabseed (data-server IDs)
                                        var serverList = document.querySelectorAll('ul.WatchServers li.server--item, ul.servers__list li, .servers-list li, .serversList li, ul.servers li, .mob-servers ul li');
                                        for(var i=0; i<serverList.length; i++) {
                                            var el = serverList[i];
                                            var serverId = el.getAttribute('data-server');
                                            var link = el.getAttribute('data-link');
                                            var name = el.querySelector('span') ? el.querySelector('span').innerText : el.innerText.trim();
                                            if (!name) name = 'سيرفر ' + (i+1);
                                            
                                            // If we already added this via data-link, skip
                                            var alreadyAdded = false;
                                            for(var j=0; j<serverItems.length; j++){ if(serverItems[j].name === name) alreadyAdded=true; }
                                            
                                            if (!alreadyAdded) {
                                                if (link && link.startsWith('http')) {
                                                    serverItems.push({ name: name, link: link });
                                                } else if (serverId !== null) {
                                                    serverItems.push({ name: name, link: window.location.href, id: serverId });
                                                } else {
                                                    serverItems.push({ name: name, link: window.location.href });
                                                }
                                            }
                                        }
                                        
                                        var watchNowBtn = document.querySelector('.watchNow button, .watchNow form button, .watch-btn, #watch-btn');
                                        if (watchNowBtn && serverItems.length === 0 && !hasIframe && !hasVideo) {
                                            watchNowBtn.click();
                                            return;
                                        }
                                        
                                        if (!isMovie && serverItems.length === 0 && !hasIframe && !hasVideo) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a');
                                            if (epLinks.length > 0) {
                                                clearInterval(intervalId);
                                                var targetEp = null;
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.trim() === epNum.toString() || text.includes(" " + epNum.toString() + " ") || text.includes("حلقة " + epNum) || text.includes("الحلقة " + epNum)) {
                                                        targetEp = epLinks[i];
                                                        break;
                                                    }
                                                }
                                                if(targetEp) {
                                                    window.location.href = targetEp.href;
                                                } else {
                                                    for(var i=0; i<epLinks.length; i++) {
                                                        if((epLinks[i].innerText || "").includes(epNum.toString())) {
                                                            targetEp = epLinks[i]; break;
                                                        }
                                                    }
                                                    window.location.href = targetEp ? targetEp.href : epLinks[0].href;
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        if (serverItems.length > 0) {
                                            clearInterval(intervalId);
                                            if (typeof AndroidBridge !== 'undefined') {
                                                // Clean up names
                                                var finalItems = [];
                                                for(var i=0; i<serverItems.length; i++){
                                                    var sName = serverItems[i].name.replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                    if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                        sName = "سيرفر " + (i+1);
                                                    }
                                                    serverItems[i].name = sName;
                                                    
                                                    // Ensure unique names
                                                    var exists = false;
                                                    for(var j=0; j<finalItems.length; j++){ if(finalItems[j].name === sName) exists = true; }
                                                    if(!exists) finalItems.push(serverItems[i]);
                                                }
                                                AndroidBridge.sendServersV2(JSON.stringify(finalItems), window.location.href);
                                            }
                                            return;
                                        }
                                        
                                        if (serverItems.length === 0 && (hasIframe || hasVideo)) {
                                            clearInterval(intervalId);
                                            if (typeof AndroidBridge !== 'undefined') {
                                                var finalItems = [{ name: "السيرفر الرئيسي", link: window.location.href }];
                                                AndroidBridge.sendServersV2(JSON.stringify(finalItems), window.location.href);
                                            }
                                            return;
                                        }
                                        
                                        // 4. Fast Fail
                                        if (!isCloudflare && document.readyState === 'complete') {
                                            window._failCount = (window._failCount || 0) + 1;
                                            if (window._failCount >= 6) {
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                                            }
                                        }
                                    }, 1500);\n                                """
    
    content = content.replace(old_js, new_js)
    
    # We need to add the sendServersV2 function inside the JavascriptInterface
    interface_code = """
                        @android.webkit.JavascriptInterface
                        fun sendServers(serversStr: String, url: String) {
"""
    new_interface_code = """
                        @android.webkit.JavascriptInterface
                        fun sendServersV2(serversJson: String, url: String) {
                            try {
                                val serversData = org.json.JSONArray(serversJson)
                                val serversNames = mutableListOf<String>()
                                val serversMap = mutableMapOf<String, String>()
                                
                                for (i in 0 until serversData.length()) {
                                    val item = serversData.getJSONObject(i)
                                    val name = item.getString("name")
                                    val link = item.getString("link")
                                    serversNames.add(name)
                                    serversMap[name] = link
                                }
                                
                                if (serversNames.isNotEmpty() && extractedServers.isEmpty()) {
                                    Handler(Looper.getMainLooper()).post {
                                        finalWatchUrl = url
                                        extractedServers = serversNames
                                        extractedServerLinks = serversMap // We will store this in a state
                                        isLoading = false
                                    }
                                }
                            } catch (e: Exception) { e.printStackTrace() }
                        }
                        
                        @android.webkit.JavascriptInterface
                        fun sendServers(serversStr: String, url: String) {
"""
    content = content.replace(interface_code, new_interface_code)

    with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
        f.write(content)

