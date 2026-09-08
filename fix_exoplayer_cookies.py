import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Make sure DefaultHttpDataSource is imported
if "import androidx.media3.datasource.DefaultHttpDataSource" not in content:
    content = content.replace("import androidx.media3.exoplayer.ExoPlayer", "import androidx.media3.exoplayer.ExoPlayer\nimport androidx.media3.datasource.DefaultHttpDataSource\nimport androidx.media3.exoplayer.source.DefaultMediaSourceFactory")

# Find where exoPlayer is built and add DefaultMediaSourceFactory
old_builder = """        ExoPlayer.Builder(context)
            .setTrackSelector(trackSelector)
            .build().apply {"""

new_builder = """        // Build ExoPlayer with cookies from WebView
        val cookie = android.webkit.CookieManager.getInstance().getCookie(uiState.currentVideoUrl ?: "") ?: ""
        val dataSourceFactory = DefaultHttpDataSource.Factory()
            .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
        if (cookie.isNotEmpty()) {
            dataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
        }
        val mediaSourceFactory = DefaultMediaSourceFactory(dataSourceFactory)
        
        ExoPlayer.Builder(context)
            .setMediaSourceFactory(mediaSourceFactory)
            .setTrackSelector(trackSelector)
            .build().apply {"""

content = content.replace(old_builder, new_builder)

# Find where setMediaItem is called and update it
old_set_media = """            val mediaItem = MediaItem.fromUri(url)
            exoPlayer.setMediaItem(mediaItem)"""

new_set_media = """            // We need to recreate the media source if the url changes to ensure new cookies are fetched
            val cookie = android.webkit.CookieManager.getInstance().getCookie(url) ?: ""
            val dataSourceFactory = DefaultHttpDataSource.Factory()
                .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
            if (cookie.isNotEmpty()) {
                dataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
            }
            val mediaSource = DefaultMediaSourceFactory(dataSourceFactory).createMediaSource(MediaItem.fromUri(url))
            
            exoPlayer.setMediaSource(mediaSource)"""

content = content.replace(old_set_media, new_set_media)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)

print("ExoPlayer cookie injection added.")
