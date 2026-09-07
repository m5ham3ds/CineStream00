import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

target = """                        if (input && !input.value) {
                            input.value = "${title.replace("'", "\\'")}";"""

new_target = """                        if (input && !input.value) {
                            input.value = "${title.replace("'", "\\'")}";
                            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                            if(btn) btn.click();
                            else if(input.form) input.form.submit();
                            return;
                        }
                    } else {
                        // Home page search form fallback for sites like animeat, topcinema, arabseed-tv
                        var isHome = false;
                        try {
                            var u = new URL(loc);
                            isHome = (u.pathname === '/' || u.pathname === '') && u.search === '';
                        } catch(e) {}
                        
                        if (isHome) {
                            var input = document.querySelector('input[name="s"], input[name="query"], input[name="keywords"], input[name="search"]');
                            if (input && !input.value) {
                                input.value = "${title.replace("'", "\\'")}";"""

content = content.replace(target, new_target)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)
print("Home search patched")
