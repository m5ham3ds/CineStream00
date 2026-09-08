import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

# Add logging
logger = """
                function logDebug(msg) {
                    if (typeof AndroidBridge !== 'undefined' && AndroidBridge.logDebug) {
                        AndroidBridge.logDebug(msg);
                    }
                }
"""

# We need to insert logger at the beginning of the script
content = content.replace("(function() {", "(function() {" + logger)

# Log finding elements
content = content.replace("var results = [];", """var results = []; logDebug('Smart Matcher running. Original title: ' + originalTitle + ' Target: ' + normTarget + ' All links count: ' + allLinks.length);""")

content = content.replace("targetResult = bestMatchElement;", """targetResult = bestMatchElement; logDebug('Found best match: ' + targetResult.href + ' with score: ' + bestMatchCount);""")

content = content.replace("setTimeout(function() { window.location.href = targetResult.href; }, 500);", """setTimeout(function() { logDebug('Navigating to ' + targetResult.href); window.location.href = targetResult.href; }, 500);""")

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    dialog_content = f.read()

bridge_func = """
                                            @android.webkit.JavascriptInterface
                                            fun logDebug(msg: String) {
                                                android.util.Log.d("AISTUDIO_DEBUG", msg)
                                            }
"""
dialog_content = dialog_content.replace("fun sendBypassStatus", bridge_func + "                                            @android.webkit.JavascriptInterface\n                                            fun sendBypassStatus")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(dialog_content)
