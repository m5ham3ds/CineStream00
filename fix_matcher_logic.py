with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_matcher = """                    var searchTarget = "${title.lowercase().replace("'", "").replace("\"", "")}";
                    var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '');
                    var words = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(' ').filter(function(w){ return w.length > 1; });"""

new_matcher = """                    var originalTitle = "${title.lowercase().replace("'", "").replace("\"", "")}";
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
                    var searchTarget = baseTitle;
                    var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '');
                    var words = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '').split(' ').filter(function(w){ return w.length > 1; });"""

old_score = """                            var matches = 0;
                            for (var j = 0; j < words.length; j++) {
                                if (linkText.includes(words[j])) matches++;
                            }"""

new_score = """                            var matches = 0;
                            for (var j = 0; j < words.length; j++) {
                                if (linkText.includes(words[j])) matches++;
                            }
                            if (isSeries && epNum) {
                                // If looking for an episode, heavily prefer links containing the episode number
                                if (linkText.includes(epNum) || results[i].innerText.includes(epNum)) {
                                    matches += 5;
                                } else if (results[i].href && results[i].href.includes(epNum)) {
                                    matches += 5;
                                }
                            }"""

content = content.replace(old_matcher, new_matcher)
content = content.replace(old_score, new_score)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
