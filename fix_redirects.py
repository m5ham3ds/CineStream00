with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

redirect_logic = """
                // --- URL TRANSFORMATION LOGIC ---
                var currentHref = window.location.href.toLowerCase();
                
                // 1. a.qfilm.tv, z1.almeshkah.net, uo.brstej.com
                if ((currentHref.includes('a.qfilm.tv') || currentHref.includes('z1.almeshkah.net') || currentHref.includes('uo.brstej.com') || currentHref.includes('e.cimalight.co')) && currentHref.includes('watch.php?vid=')) {
                    if (currentHref.includes('e.cimalight.co')) {
                        // cimalight watch.php -> click the embed or video to get iframe url
                        // handled by extractor below automatically
                    } else {
                        window.location.href = window.location.href.replace('watch.php', 'play.php');
                        return;
                    }
                }
                // 2. laaroza.space
                if (currentHref.includes('laaroza.') && currentHref.includes('video.php?vid=')) {
                    window.location.href = window.location.href.replace('video.php', 'play.php');
                    return;
                }
                // 3. arabseed, topcinema, arabseed-tv
                if ((currentHref.includes('arabseed.wine') || currentHref.includes('topcinema.io') || currentHref.includes('arabseed-tv.com')) 
                    && !currentHref.includes('?s=') && !currentHref.includes('search') && !currentHref.includes('/watch') && !currentHref.includes('/page/')) {
                    // Check if it's the info page
                    var watchLink = document.querySelector('a.watchBtn, a.btn-watch, a[href*="/watch"]');
                    if (watchLink && watchLink.href.includes('/watch')) {
                        window.location.href = watchLink.href;
                        return;
                    } else {
                        // Append /watch/ to the URL
                        var newUrl = window.location.href;
                        if (!newUrl.endsWith('/')) newUrl += '/';
                        window.location.href = newUrl + 'watch/';
                        return;
                    }
                }
                // 4. animeblkom.net
                if (currentHref.includes('animeblkom.net/anime/')) {
                    window.location.href = window.location.href.replace('/anime/', '/watch/') + '/0';
                    return;
                }
                // 5. stardima.com
                if (currentHref.includes('stardima.com/tvshow/') && !currentHref.includes('/play/')) {
                    var stardimaPlay = document.querySelector('a[href*="/play/"]');
                    if (stardimaPlay) {
                        window.location.href = stardimaPlay.href;
                        return;
                    }
                }
"""

# Insert this after var loc = window.location.href.toLowerCase();
search_str = "var loc = window.location.href.toLowerCase();"
if search_str in content:
    content = content.replace(search_str, search_str + redirect_logic)
else:
    print("Could not find the insertion point!")

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
