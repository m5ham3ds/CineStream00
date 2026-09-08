import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_block = """        // Wait for up to 15 seconds, but check every 1 second if servers were found
        var waited = 0
        while (waited < 15) {
            delay(1000)
            waited++
            if (extractedServers.isNotEmpty()) {
                // Servers found! We can stop waiting.
                return@LaunchedEffect
            }
        }
        
        // If we waited 30 seconds and still no servers, move to the next site
        if (extractedServers.isEmpty()) {
            currentSiteIndex++
        }"""

new_block = """        // Wait for up to 30 iterations, but pause counting if we are doing Cloudflare bypass
        var waited = 0
        while (waited < 30) {
            delay(1000)
            if (bypassStatus != "CLOUDFLARE" && bypassStatus != "CHECKING_CLOUDFLARE") {
                waited++
            }
            if (extractedServers.isNotEmpty()) {
                // Servers found! We can stop waiting.
                return@LaunchedEffect
            }
            if (isFailed) {
                return@LaunchedEffect
            }
        }
        
        // If we timed out and still no servers, move to the next site
        if (extractedServers.isEmpty()) {
            currentSiteIndex++
        }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Replaced timeout block successfully!")
else:
    print("Could not find timeout block!")
