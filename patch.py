with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    lines = f.readlines()

fail_logic_site = """
                if (!isCloudflare && document.readyState === 'complete') {
                    window._failCount = (window._failCount || 0) + 1;
                    var maxFails = (loc.includes('?s=') || loc.includes('search') || loc.includes('query=') || loc.includes('keywords=')) ? 2 : 4;
                    if (window._failCount >= maxFails) { 
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                    }
                }
"""

fail_logic_extractor = """
                if (!isCloudflare && document.readyState === 'complete') {
                    window._failCount = (window._failCount || 0) + 1;
                    if (window._failCount >= 4) { 
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                    }
                }
"""

lines.insert(448, fail_logic_site)
lines.insert(520, fail_logic_extractor)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.writelines(lines)
