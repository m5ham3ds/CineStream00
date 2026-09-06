import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

old_code = """    LaunchedEffect(currentQuality) {
        val parametersBuilder = trackSelector.buildUponParameters()
        when (currentQuality) {
            "360p" -> parametersBuilder.setMaxVideoSize(Int.MAX_VALUE, 360)
            "480p" -> parametersBuilder.setMaxVideoSize(Int.MAX_VALUE, 480)
            "720p" -> parametersBuilder.setMaxVideoSize(Int.MAX_VALUE, 720)
            "1080p" -> parametersBuilder.setMaxVideoSize(Int.MAX_VALUE, 1080)
            "4K" -> parametersBuilder.setMaxVideoSize(Int.MAX_VALUE, 2160)
            "Auto" -> parametersBuilder.clearVideoSizeConstraints()
            else -> parametersBuilder.clearVideoSizeConstraints()
        }
        trackSelector.setParameters(parametersBuilder)
    }"""

new_code = """    LaunchedEffect(currentQuality) {
        val parametersBuilder = trackSelector.buildUponParameters()
        if (currentQuality == "Auto") {
            parametersBuilder.clearVideoSizeConstraints()
        } else {
            val height = currentQuality.replace("p", "").toIntOrNull()
            if (height != null) {
                // To force a specific quality, we set max and min to the same height,
                // or just max and clear others, but ExoPlayer usually respects max size constraints well.
                // We will set both max and min video size to force this exact resolution if available.
                parametersBuilder.setMaxVideoSize(Int.MAX_VALUE, height)
                parametersBuilder.setMinVideoSize(0, height)
            } else {
                parametersBuilder.clearVideoSizeConstraints()
            }
        }
        trackSelector.setParameters(parametersBuilder)
    }"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
