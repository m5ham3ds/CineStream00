import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

# Add missing imports for WindowInsetsControllerCompat and DefaultTrackSelector
missing_imports = """
import androidx.core.view.WindowInsetsControllerCompat
import androidx.core.view.WindowInsetsCompat
import androidx.media3.exoplayer.trackselection.DefaultTrackSelector
"""

import_insert_pos = content.find("import androidx.media3.exoplayer.ExoPlayer\n") + len("import androidx.media3.exoplayer.ExoPlayer\n")
content = content[:import_insert_pos] + missing_imports + content[import_insert_pos:]

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
