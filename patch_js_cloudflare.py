with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

import re

# We need to replace the checkJS javascript to also send CLOUDFLARE status
pattern = re.compile(r'val checkJS = """(.*?)return \(urlChanged \|\| !challengeExists\) && contentExists;\s*\}\)\(\);\s*"""\.trimIndent\(\)', re.DOTALL)

new_js = """val checkJS = \"\"\"
                                                    (function() {
                                                        var urlChanged = window.location.href.indexOf('cf_chl') === -1 && 
                                                                         window.location.href.indexOf('challenge') === -1 &&
                                                                         window.location.href.indexOf('__cf') === -1;

                                                        var challengeExists = document.getElementById('challenge-running') !== null ||
                                                                              document.querySelector('.cf-browser-verification') !== null ||
                                                                              document.body.innerText.indexOf('Checking your browser') !== -1 ||
                                                                              document.title.toLowerCase().indexOf('just a moment') !== -1;

                                                        var contentExists = document.querySelector('video') !== null ||
                                                                            document.querySelector('.download-btn') !== null ||
                                                                            document.getElementById('player-container') !== null ||
                                                                            document.querySelector('iframe') !== null ||
                                                                            document.querySelector('a') !== null;
                                                                            
                                                        if (challengeExists && !contentExists) {
                                                            try { AndroidBridge.sendBypassStatus('CLOUDFLARE'); } catch (e) {}
                                                        }

                                                        return (urlChanged || !challengeExists) && contentExists;
                                                    })();
                                                \"\"\".trimIndent()"""

content = pattern.sub(new_js, content)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
