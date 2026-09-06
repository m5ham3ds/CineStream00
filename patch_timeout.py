import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

extractor_str = """        // Hidden Extractor for Quality
        if (isExtractingQuality && selectedServerForQuality != null) {"""
        
extractor_str_new = """        // Hidden Extractor for Quality
        if (isExtractingQuality && selectedServerForQuality != null) {
            LaunchedEffect(selectedServerForQuality) {
                kotlinx.coroutines.delay(12000)
                if (isExtractingQuality && extractedQualities.isEmpty()) {
                    val serverUrl = extractedServerLinks[selectedServerForQuality] ?: finalWatchUrl ?: searchUrl
                    extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("جودة أصلية (Default)", serverUrl))
                    isExtractingQuality = false
                }
            }"""

content = content.replace(extractor_str, extractor_str_new)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("Timeout patched")
