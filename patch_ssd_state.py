import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Add states
old_state = """    var finalWatchUrl by remember { mutableStateOf<String?>(null) }
    var isFailed by remember { mutableStateOf(false) }
    var bypassStatus by remember { mutableStateOf("CHECKING_CLOUDFLARE") }"""

new_state = """    var finalWatchUrl by remember { mutableStateOf<String?>(null) }
    var isFailed by remember { mutableStateOf(false) }
    var bypassStatus by remember { mutableStateOf("CHECKING_CLOUDFLARE") }

    val coroutineScope = rememberCoroutineScope()
    var selectedServerToExtract by remember { mutableStateOf<String?>(null) }
    var selectedServerUrlToExtract by remember { mutableStateOf<String?>(null) }
    var isExtractingQualities by remember { mutableStateOf(false) }
    var availableQualities by remember { mutableStateOf<List<com.example.utils.M3U8Parser.QualityInfo>>(emptyList()) }"""

content = content.replace(old_state, new_state)

# Add HiddenVideoExtractor logic inside the dialog, just below `AndroidView` (or anywhere in the UI tree, e.g., at the end of the Box)
# Actually, it's better to put it at the very top of the Dialog content, outside the visible Box.
# Let's see the structure.
old_box = """    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box("""

new_box = """    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        if (isExtractingQualities && selectedServerUrlToExtract != null) {
            HiddenVideoExtractor(
                url = selectedServerUrlToExtract!!,
                isMovie = isMovie,
                season = season,
                episode = episode,
                targetServer = selectedServerToExtract,
                onVideoUrlFound = { videoUrl ->
                    coroutineScope.launch {
                        val qualities = com.example.utils.M3U8Parser.getQualities(videoUrl)
                        availableQualities = qualities
                        isExtractingQualities = false
                    }
                },
                onIframeUrlFound = { iframeUrl ->
                    selectedServerUrlToExtract = iframeUrl
                },
                onServersFound = {}
            )
        }
        
        Box("""

content = content.replace(old_box, new_box)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

