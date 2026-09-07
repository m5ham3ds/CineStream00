import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

# Update method signature
content = content.replace(
    'fun getScriptForSite(siteName: String, isMovie: Boolean, episode: Int): String {',
    'fun getScriptForSite(siteName: String, isMovie: Boolean, episode: Int, title: String): String {'
)

# Replace the initial cloudflare check
old_cf = """                var isCloudflare = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                if (isCloudflare || cf) {"""

new_cf = """                var isCloudflareTitle = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                var bodyText = document.body ? document.body.innerText : "";
                var isCloudflareText = bodyText.includes('Performing security verification') || bodyText.includes('protect against malicious bots') || bodyText.includes('verifies you are not a bot');
                var isCloudflare = isCloudflareTitle || isCloudflareText;
                var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                
                if (isCloudflare || cf) {"""
content = content.replace(old_cf, new_cf)

# Find where `if (!isCloudflare && document.readyState === 'complete') {` begins to insert the search logic
# Wait, let's insert it before the iframe logic or just after the site specific logic.
# After `if (serverItems.length > 0) { ... }`

old_search_logic_placeholder = """                if (serverItems.length > 0) {
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
                }"""

new_search_logic = old_search_logic_placeholder + """
                
                // --- SMART SEARCH RESULT MATCHER ---
                if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie'))) {
                    // Try to find the exact movie/anime in search results
                    var searchTarget = "${title.lowercase().replace("'", "\\'")}";
                    var results = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0, .GridItem a');
                    
                    if (results && results.length > 0) {
                        var targetResult = null;
                        
                        // First try exact or near-exact match on innerText or title attribute
                        for (var i = 0; i < results.length; i++) {
                            var linkText = (results[i].innerText || '') + " " + (results[i].getAttribute('title') || '');
                            linkText = linkText.toLowerCase().replace(/[^a-z0-9 ]/g, ''); // normalize
                            var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '');
                            
                            if (linkText.includes(normTarget)) {
                                targetResult = results[i];
                                break;
                            }
                        }
                        
                        // Fallback: match by most words
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
                            // If we matched most words (or at least all but one)
                            if (words.length > 0 && bestMatchCount >= Math.max(1, words.length - 1)) {
                                targetResult = bestMatchElement;
                            }
                        }
                        
                        // Fallback: if it's explicitly a search page, just take the first result
                        if (!targetResult && (loc.includes('?s=') || loc.includes('search') || loc.includes('query=') || loc.includes('keywords=') || loc.includes('?search_param='))) {
                            targetResult = results[0];
                        }
                        
                        if (targetResult) {
                            // Let the page navigate to this detail page. The script will re-inject and find servers.
                            window.location.href = targetResult.href;
                            return;
                        }
                    } else if (loc.includes('searchq') || loc.includes('search')) {
                        // Some sites might require submitting a form if they are purely a search endpoint
                        var input = document.querySelector('input[name="s"], input[name="query"], input[name="keywords"]');
                        if (input && !input.value) {
                            input.value = "${title.replace("'", "\\'")}";
                            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                            if(btn) btn.click();
                            else if(input.form) input.form.submit();
                            return;
                        }
                    }
                }
"""
content = content.replace(old_search_logic_placeholder, new_search_logic)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)
print("SiteScripts.kt patched")
