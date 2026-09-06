import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_code = """    LaunchedEffect(currentSiteIndex) {
        if (currentSiteIndex >= prioritySites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentSiteName = prioritySites[currentSiteIndex]
        bypassStatus = "CHECKING_CLOUDFLARE"
        
        val baseUrl = if (searchUrl.contains(prioritySites[currentSiteIndex])) searchUrl else {
            val isMovieParam = if (isMovie) "true" else "false"
            val targetUrl = "https://${prioritySites[currentSiteIndex]}/?s=${java.net.URLEncoder.encode(title, "UTF-8")}"
            targetUrl
        }
        currentUrl = baseUrl
    }"""

new_code = """    LaunchedEffect(currentSiteIndex) {
        if (currentSiteIndex >= prioritySites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentSiteName = prioritySites[currentSiteIndex]
        bypassStatus = "CHECKING_CLOUDFLARE"
        
        val baseUrl = if (searchUrl.contains(prioritySites[currentSiteIndex])) searchUrl else {
            val isMovieParam = if (isMovie) "true" else "false"
            val targetUrl = "https://${prioritySites[currentSiteIndex]}/?s=${java.net.URLEncoder.encode(title, "UTF-8")}"
            targetUrl
        }
        currentUrl = baseUrl
    }

    LaunchedEffect(isExtractingQualities) {
        if (isExtractingQualities) {
            kotlinx.coroutines.delay(15000) // 15 seconds timeout
            if (isExtractingQualities) {
                isExtractingQualities = false
                // Fallback to playing the URL directly if extraction fails
                selectedServerUrlToExtract?.let { url ->
                    onPlay(url, selectedServerToExtract ?: "سيرفر", currentSiteName)
                }
            }
        }
    }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

