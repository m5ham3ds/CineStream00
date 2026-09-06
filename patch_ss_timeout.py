import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

old_code = """                if (!isCloudflare && document.readyState === 'complete') {
                    window._failCount = (window._failCount || 0) + 1;
                    if (window._failCount >= 8) { // 12 seconds
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                    }
                }"""

new_code = """                if (!isCloudflare && document.readyState === 'complete') {
                    var loc = window.location.href.toLowerCase();
                    var hasSearch = loc.includes('?s=') || loc.includes('?keywords=') || loc.includes('?search') || loc.includes('?query=');
                    var isHome = loc.endsWith('/') && !hasSearch;
                    
                    var pageText = document.body ? document.body.innerText : "";
                    var notFound = pageText.includes("لا توجد نتائج") || pageText.includes("لم يتم العثور") || pageText.includes("لا يوجد") || pageText.includes("الصفحة غير موجودة") || pageText.includes("404") || pageText.includes("not found");

                    // If redirected to home page (lost search query) or explicitly no results found, fail instantly.
                    if (isHome || notFound) {
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                        return;
                    }

                    // Otherwise wait up to 4 intervals (6 seconds) before giving up
                    window._failCount = (window._failCount || 0) + 1;
                    if (window._failCount >= 4) { 
                        clearInterval(intervalId);
                        if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                    }
                }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)

