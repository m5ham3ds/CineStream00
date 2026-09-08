import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_cf = """                        if (cf) {
                            cf.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);z-index:9999999;';
                            if (cf.parentElement && cf.parentElement !== document.body) {
                                cf.parentElement.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);z-index:9999999;';
                            }
                        }"""

new_cf = """                        if (cf) {
                            cf.style.position = 'fixed';
                            cf.style.top = '50%';
                            cf.style.left = '50%';
                            cf.style.transform = 'translate(-50%, -50%)';
                            cf.style.zIndex = '9999999';
                            cf.style.visibility = 'visible';
                            if (cf.parentElement && cf.parentElement !== document.body) {
                                cf.parentElement.style.position = 'fixed';
                                cf.parentElement.style.top = '50%';
                                cf.parentElement.style.left = '50%';
                                cf.parentElement.style.transform = 'translate(-50%, -50%)';
                                cf.parentElement.style.zIndex = '9999999';
                                cf.parentElement.style.visibility = 'visible';
                            }
                        }"""

content = content.replace(old_cf, new_cf)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
print("Updated CF styles.")
