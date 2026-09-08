import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_query = """                    for(var k=0; k<allLinks.length; k++){
                        var h = allLinks[k].href || "";
                        h = h.toLowerCase();
                        if(h && h.startsWith('http') && !h.includes('login') && !h.includes('register') && !h.includes('?s=') && !h.includes('search') && !h.includes('keywords=') && !h.includes('category')){
                            results.push(allLinks[k]);
                        }
                    }"""

new_query = """                    for(var k=0; k<allLinks.length; k++){
                        var h = allLinks[k].href || "";
                        h = h.toLowerCase();
                        // Less restrictive filtering to catch links in dynamic search result grids
                        if(h && h.startsWith('http') && !h.includes('login') && !h.includes('register') && !h.includes('category')){
                            results.push(allLinks[k]);
                        }
                    }"""

content = content.replace(old_query, new_query)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
