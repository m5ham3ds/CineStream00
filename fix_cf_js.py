import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

pattern = re.compile(r'val checkJS = """\s*\(function\(\) \{.*?\}\)\(\);\s*"""\.trimIndent\(\)', re.DOTALL)

new_js = """val checkJS = \"\"\"
                                                    (function() {
                                                        var isCloudflare = document.getElementById('challenge-running') !== null ||
                                                                           document.querySelector('.cf-browser-verification') !== null ||
                                                                           document.querySelector('#cf-wrapper') !== null ||
                                                                           document.querySelector('#turnstile-wrapper') !== null ||
                                                                           document.body.innerHTML.indexOf('cf-turnstile') !== -1 ||
                                                                           document.title.toLowerCase().indexOf('just a moment') !== -1 ||
                                                                           document.title.toLowerCase().indexOf('attention required') !== -1 ||
                                                                           document.body.innerText.indexOf('Checking your browser') !== -1 ||
                                                                           document.body.innerText.indexOf('Verify you are human') !== -1;

                                                        if (isCloudflare) {
                                                            try { AndroidBridge.sendBypassStatus('CLOUDFLARE'); } catch (e) {}
                                                            return false;
                                                        }

                                                        // If we are here, it's not Cloudflare.
                                                        // Check if real content exists to be sure the page is loaded
                                                        var contentExists = document.querySelector('video') !== null ||
                                                                            document.querySelector('iframe') !== null ||
                                                                            document.querySelector('.download-btn') !== null ||
                                                                            document.getElementById('player-container') !== null ||
                                                                            document.body.innerText.length > 200; // Real pages have text

                                                        return contentExists;
                                                    })();
                                                \"\"\".trimIndent()"""

content = pattern.sub(new_js, content)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
