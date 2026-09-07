with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

import re
start_idx = content.find("fun PlayerScreen")
if start_idx != -1:
    # go back to the @Composable annotation if it exists
    comp_idx = content.rfind("@Composable", 0, start_idx)
    if comp_idx != -1:
        start_idx = comp_idx
    
    # go back to the @OptIn if it exists
    opt_idx = content.rfind("@OptIn", 0, start_idx)
    if opt_idx != -1:
        start_idx = opt_idx

    rest_of_file = content[start_idx:]
    
    header = """package com.example.ui.screens.player

import android.app.Activity
import android.content.pm.ActivityInfo
import android.webkit.WebSettings
import android.webkit.WebView
import androidx.annotation.OptIn
import androidx.compose.animation.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.detectDragGestures
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.List
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.media3.exoplayer.ExoPlayer

"""
    
    with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
        f.write(header + rest_of_file)
    print("Rewrote header")
else:
    print("Could not find start index")
