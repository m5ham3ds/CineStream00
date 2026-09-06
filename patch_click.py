import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

old_click = """                            if(targetEp) {
                                clearInterval(intervalId);
                                window.location.href = targetEp.href;
                                return;
                            }"""

new_click = """                            if(targetEp) {
                                clearInterval(intervalId);
                                var onclickAttr = targetEp.getAttribute('onclick');
                                if (onclickAttr && onclickAttr.includes('openEpisode(')) {
                                    var match = onclickAttr.match(/openEpisode\('([^']+)'\)/);
                                    if (match) {
                                        window.location.href = atob(match[1]);
                                        return;
                                    }
                                }
                                window.location.href = targetEp.href;
                                return;
                            }"""

if old_click in content:
    content = content.replace(old_click, new_click)
    with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
        f.write(content)
    print("Patched click successfully.")
else:
    print("Could not find old_click")

