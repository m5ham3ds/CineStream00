with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

# Completely rewrite the top lines safely
import re
content = re.sub(r'^package.*?(?=import androidx\.compose)', 
"""package com.example.ui.screens.player

import android.webkit.WebView
import android.webkit.WebSettings
import android.app.Activity
import android.content.pm.ActivityInfo
import androidx.annotation.OptIn
""", content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)
