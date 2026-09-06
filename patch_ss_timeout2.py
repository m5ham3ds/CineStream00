import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

old_code = """                    var loc = window.location.href.toLowerCase();
                    var hasSearch = loc.includes('?s=') || loc.includes('?keywords=') || loc.includes('?search') || loc.includes('?query=');
                    var isHome = loc.endsWith('/') && !hasSearch;"""

new_code = """                    var loc = window.location.href.toLowerCase();
                    var hasSearch = loc.includes('?s=') || loc.includes('?keywords=') || loc.includes('?search') || loc.includes('?query=');
                    
                    var isHome = false;
                    try {
                        var u = new URL(loc);
                        isHome = (u.pathname === '/' || u.pathname === '') && u.search === '';
                    } catch(e) {}"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)

