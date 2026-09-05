import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_delay = """        // 25 seconds timeout per site to account for Cloudflare
        delay(25000)
        if (extractedServers.isEmpty()) {
            currentSiteIndex++
        }"""

new_delay = """        // Wait for up to 30 seconds, but check every 1 second if servers were found
        var waited = 0
        while (waited < 30) {
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

content = content.replace(old_delay, new_delay)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

