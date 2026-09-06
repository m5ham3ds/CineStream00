import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

old_qfilm = """                else if ("$siteName" === "a.qfilm.tv") {
                    var serverArray = window.servers;
                    if (serverArray && Array.isArray(serverArray)) {
                        var buttons = document.querySelectorAll('.server-btn');
                        var names = [];
                        buttons.forEach(function(btn) { names.push(btn.innerText.trim()); });
                        for (var i = 0; i < serverArray.length; i++) {
                            var iframeHtml = serverArray[i];
                            var srcMatch = iframeHtml.match(/src=["']([^"']+)["']/);
                            if (srcMatch) {
                                var name = (i < names.length && names[i]) ? names[i] : ('سيرفر ' + (i+1));
                                serverItems.push({ name: name, link: srcMatch[1] });
                            }
                        }
                    }
                }"""

new_qfilm = """                else if ("$siteName" === "a.qfilm.tv") {
                    var serverArray = window.servers;
                    if (!serverArray && typeof servers !== 'undefined') serverArray = servers;
                    if (serverArray && Array.isArray(serverArray)) {
                        var buttons = document.querySelectorAll('.server-btn');
                        var names = [];
                        buttons.forEach(function(btn) { names.push(btn.innerText.trim()); });
                        for (var i = 0; i < serverArray.length; i++) {
                            var iframeHtml = serverArray[i];
                            var srcMatch = iframeHtml.match(/src=["']([^"']+)["']/);
                            if (srcMatch) {
                                var name = (i < names.length && names[i]) ? names[i] : ('سيرفر ' + (i+1));
                                serverItems.push({ name: name, link: srcMatch[1] });
                            }
                        }
                    }
                }"""

content = content.replace(old_qfilm, new_qfilm)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)
print("Patched qfilm")
