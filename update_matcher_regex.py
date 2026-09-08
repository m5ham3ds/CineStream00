import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

pattern = re.compile(r'// --- SMART SEARCH RESULT MATCHER ---.*?}(?=\s*if \(serverItems\.length > 0)', re.DOTALL)
match = pattern.search(content)

new_block = """// --- SMART SEARCH RESULT MATCHER ---
                if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie') && !loc.includes('play.php') && !loc.includes('video.php') && !loc.includes('/anime/') && !loc.includes('tvshow'))) {
                    var originalTitle = "${title.lowercase().replace("'", "").replace("\"", "")}";
                    var isSeries = originalTitle.includes(' - s') && originalTitle.includes('e');
                    var baseTitle = originalTitle;
                    var epNum = "";
                    if (isSeries) {
                        var parts = originalTitle.split(' - s');
                        baseTitle = parts[0].trim();
                        var rightSide = parts[1] || "";
                        if (rightSide.includes('e')) {
                            epNum = rightSide.split('e')[1].trim();
                        }
                    }
                    var searchTarget = baseTitle;
                    var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '');
                    var words = normTarget.split(' ').filter(function(w){ return w.length > 1; });
                    
                    var allLinks = document.querySelectorAll('a');
                    var results = [];
                    for(var k=0; k<allLinks.length; k++){
                        var h = allLinks[k].href || "";
                        h = h.toLowerCase();
                        if(h && h.startsWith('http') && !h.includes('login') && !h.includes('register') && !h.includes('?s=') && !h.includes('search') && !h.includes('keywords=') && !h.includes('category')){
                            results.push(allLinks[k]);
                        }
                    }
                    
                    if (results.length > 0) {
                        var targetResult = null;
                        var bestMatchCount = 0;
                        var bestMatchElement = null;
                        for (var i = 0; i < results.length; i++) {
                            var linkText = (results[i].innerText || '') + " " + (results[i].getAttribute('title') || '');
                            var linkHref = results[i].href || '';
                            linkText = linkText.toLowerCase().replace(/[^a-z0-9 ]/g, '');
                            
                            var matchCount = 0;
                            // Exact title match gets huge bonus
                            if (linkText.includes(normTarget)) {
                                matchCount += 20;
                            } else {
                                for(var w = 0; w < words.length; w++) {
                                    if (linkText.includes(words[w])) matchCount++;
                                }
                            }
                            
                            // If it contains an image, it's more likely a media card
                            if (results[i].querySelector('img')) {
                                matchCount += 2;
                            }
                            
                            if (isSeries && epNum) {
                                if (linkText.includes(epNum)) {
                                    matchCount += 10;
                                } else if (linkHref.includes(epNum)) {
                                    matchCount += 5;
                                } else if (linkHref.includes('season') || linkHref.includes('series') || linkHref.includes('episode')) {
                                    matchCount += 3;
                                }
                            }
                            
                            if (matchCount > bestMatchCount) {
                                bestMatchCount = matchCount;
                                bestMatchElement = results[i];
                            }
                        }
                        
                        if (bestMatchCount >= Math.max(1, words.length)) {
                            targetResult = bestMatchElement;
                        }
                        
                        if (!targetResult && (loc.includes('?s=') || loc.includes('search') || loc.includes('query=') || loc.includes('keywords=') || loc.includes('?search_param='))) {
                            // fallback
                            var oldResults = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0, .GridItem a');
                            if(oldResults && oldResults.length > 0) {
                                targetResult = oldResults[0];
                            }
                        }
                        
                        if (targetResult) {
                            window.location.href = targetResult.href;
                            return;
                        }
                    } else if (loc.includes('searchq') || loc.includes('search') || loc.includes('?s=')) {
                        var input = document.querySelector('input[name="s"], input[name="query"], input[name="keywords"], input[name="search"]');
                        if (input && !input.value) {
                            input.value = "${title.replace("'", "").replace("\"", "")}";
                            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                            if (btn) btn.click();
                        }
                    }
                }
                """

if match:
    content = content[:match.start()] + new_block + content[match.end():]
    with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find regex match")
