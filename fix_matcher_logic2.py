with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_searchTarget = """                    var searchTarget = "${title.lowercase().replace("'", "").replace("\"", "")}";"""

new_searchTarget = """                    var originalTitle = "${title.lowercase().replace("'", "").replace("\"", "")}";
                    var isSeries = originalTitle.includes(' - s') && originalTitle.includes('e');
                    var baseTitle = originalTitle;
                    var epNum = "";
                    if (isSeries) {
                        var parts = originalTitle.split(' - s');
                        baseTitle = parts[0].trim();
                        if (parts[1] && parts[1].includes('e')) {
                            epNum = parts[1].split('e')[1].trim();
                        }
                    }
                    var searchTarget = baseTitle;"""

content = content.replace(old_searchTarget, new_searchTarget)

old_matchCount = """                                var matchCount = 0;
                                for (var j = 0; j < words.length; j++) {
                                    if (linkText.includes(words[j])) matchCount++;
                                }"""

new_matchCount = """                                var matchCount = 0;
                                for (var j = 0; j < words.length; j++) {
                                    if (linkText.includes(words[j])) matchCount++;
                                }
                                if (isSeries && epNum) {
                                    if (linkText.includes(epNum) || results[i].innerText.includes(epNum)) {
                                        matchCount += 10;
                                    } else if (results[i].href && results[i].href.includes(epNum)) {
                                        matchCount += 5;
                                    }
                                }"""

content = content.replace(old_matchCount, new_matchCount)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
