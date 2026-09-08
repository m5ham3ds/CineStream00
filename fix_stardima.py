with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

stardima_old = """                // 5. stardima.com
                if (currentHref.includes('stardima.com/tvshow/') && !currentHref.includes('/play/')) {
                    var stardimaPlay = document.querySelector('a[href*="/play/"]');
                    if (stardimaPlay) {
                        window.location.href = stardimaPlay.href;
                        return;
                    }
                }"""

stardima_new = """                // 5. stardima.com
                if (currentHref.includes('stardima.com/tvshow/') && !currentHref.includes('/play/')) {
                    var episodeLinks = document.querySelectorAll('a[href*="/play/"]');
                    if (episodeLinks.length > 0) {
                        var targetLink = episodeLinks[0];
                        if (!${isMovie}) {
                            var targetEpStr = "حلقة ${episode}";
                            for (var i = 0; i < episodeLinks.length; i++) {
                                var txt = episodeLinks[i].innerText || "";
                                if (txt.includes(targetEpStr) || txt.includes(targetEpStr.replace('حلقة ', 'الحلقة '))) {
                                    targetLink = episodeLinks[i];
                                    break;
                                }
                            }
                        }
                        window.location.href = targetLink.href;
                        return;
                    }
                }"""

content = content.replace(stardima_old, stardima_new)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
