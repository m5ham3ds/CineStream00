import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

# Add states for available video tracks
state_add = """    var showInitialSelection by remember { mutableStateOf(false) }

    // State to hold actual available qualities from ExoPlayer
    var availableVideoQualities by remember { mutableStateOf<List<String>>(listOf("Auto")) }
"""
content = content.replace("    var showInitialSelection by remember { mutableStateOf(false) }", state_add)

# Add ExoPlayer listener to populate available video qualities
exo_listener = """    val listener = remember {
        object : Player.Listener {
            override fun onTracksChanged(tracks: Tracks) {
                super.onTracksChanged(tracks)
                val qualities = mutableSetOf<String>()
                qualities.add("Auto")
                
                for (trackGroup in tracks.groups) {
                    if (trackGroup.type == androidx.media3.common.C.TRACK_TYPE_VIDEO) {
                        for (i in 0 until trackGroup.length) {
                            val format = trackGroup.getTrackFormat(i)
                            if (format.height > 0) {
                                qualities.add("${format.height}p")
                            }
                        }
                    }
                }
                availableVideoQualities = qualities.toList().sortedByDescending { 
                    if (it == "Auto") Int.MAX_VALUE else it.replace("p", "").toIntOrNull() ?: 0 
                }
            }
            
            override fun onPlaybackStateChanged(state: Int) {
                if (state == Player.STATE_READY && !isPlaying) {
                    isPlaying = exoPlayer.playWhenReady
                }
            }
            override fun onIsPlayingChanged(isPlay: Boolean) {
                isPlaying = isPlay
            }
            override fun onPositionDiscontinuity(
                oldPosition: Player.PositionInfo,
                newPosition: Player.PositionInfo,
                reason: Int
            ) {
                currentTime = exoPlayer.currentPosition
            }
        }
    }
    
    DisposableEffect(exoPlayer) {
        exoPlayer.addListener(listener)
        onDispose {
            exoPlayer.removeListener(listener)
        }
    }"""

# Find the existing listener and replace it
old_listener = """    DisposableEffect(exoPlayer) {
        val listener = object : Player.Listener {
            override fun onPlaybackStateChanged(state: Int) {
                if (state == Player.STATE_READY && !isPlaying) {
                    isPlaying = exoPlayer.playWhenReady
                }
            }
            override fun onIsPlayingChanged(isPlay: Boolean) {
                isPlaying = isPlay
            }
            override fun onPositionDiscontinuity(
                oldPosition: Player.PositionInfo,
                newPosition: Player.PositionInfo,
                reason: Int
            ) {
                currentTime = exoPlayer.currentPosition
            }
        }
        exoPlayer.addListener(listener)
        onDispose {
            exoPlayer.removeListener(listener)
        }
    }"""
content = content.replace(old_listener, exo_listener)

# Replace the hardcoded list with the dynamic one in the QualitySheet
old_sheet = """                val qualities = listOf("Auto", "4K", "1080p", "720p", "480p", "360p")
                qualities.forEach { q ->"""
new_sheet = """                availableVideoQualities.forEach { q ->"""
content = content.replace(old_sheet, new_sheet)

# Also in the initial selection Dialog if it's there
old_initial = """                        androidx.compose.foundation.lazy.LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            items(listOf("Auto", "1080p", "720p", "480p")) { q ->"""
new_initial = """                        androidx.compose.foundation.lazy.LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                            items(availableVideoQualities) { q ->"""
content = content.replace(old_initial, new_initial)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)

