package com.example.ui.screens.player

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Brush
import androidx.compose.foundation.border
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.ui.draw.clip
import androidx.compose.material.icons.outlined.CloudDownload
import androidx.compose.material.icons.outlined.Security
import androidx.compose.material.icons.outlined.Sync
import androidx.compose.material.icons.outlined.Storage
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.sp
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.net.URLEncoder

@SuppressLint("SetJavaScriptEnabled")
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ServerSelectionDialog(
    title: String,
    isMovie: Boolean,
    season: Int = 1,
    episode: Int = 1,
    isAnime: Boolean = false,
    onDismiss: () -> Unit,
    onPlay: (url: String, serverName: String, website: String) -> Unit
) {
    val coroutineScope = rememberCoroutineScope()
    
    val priorityAnimeSites = listOf("witanime.you", "w1.anime4up.rest", "animeblkom.net", "animeat.net", "arabanime.net", "det.animerco.org", "vip.animeluxe.org")
    val priorityMovieSites = listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", "topcinema.io", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", "stardima.com", "watch.stardima.com", "uo.brstej.com", "laaroza.space")
    val prioritySeriesSites = listOf("topcinema.io", "stardima.com", "tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", "watch.stardima.com", "uo.brstej.com", "laaroza.space")

    val prioritySites = if (isAnime) priorityAnimeSites else if (isMovie) priorityMovieSites else prioritySeriesSites

    var currentSiteIndex by remember { mutableStateOf(0) }
    var currentSiteName by remember { mutableStateOf(prioritySites[0]) }
    
    var isLoading by remember { mutableStateOf(true) }
    var loadingMessage by remember { mutableStateOf("جاري الفحص وتخطي الحماية...") }
    
    var extractedServers by remember { mutableStateOf<List<String>>(emptyList()) }
    var extractedServerLinks by remember { mutableStateOf<Map<String, String>>(emptyMap()) }
    var finalWatchUrl by remember { mutableStateOf<String?>(null) }
    var isFailed by remember { mutableStateOf(false) }
    var bypassStatus by remember { mutableStateOf("CHECKING_CLOUDFLARE") }

    LaunchedEffect(currentSiteIndex) {
        if (currentSiteIndex >= prioritySites.size) {
            isLoading = false
            isFailed = true
            return@LaunchedEffect
        }
        
        currentSiteName = prioritySites[currentSiteIndex]
        bypassStatus = "CHECKING_CLOUDFLARE"
        loadingMessage = "جاري الفحص في موقع $currentSiteName..."
        extractedServers = emptyList()
        finalWatchUrl = null
        
        // Wait for up to 30 seconds, but check every 1 second if servers were found
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
        }
    }

    val encodedTitle = URLEncoder.encode(title, "UTF-8")
    val searchUrl = when (currentSiteName) {
        "tv10.egydead.live" -> "https://tv10.egydead.live/page/1/?s=$encodedTitle"
        "a.qfilm.tv" -> "https://a.qfilm.tv/search.php?keywords=$encodedTitle"
        "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
        "arabseed.wine" -> "https://www.arabseed.wine/page/1/?s=$encodedTitle"
        "topcinema.io" -> "https://topcinema.io/search.php?keywords=$encodedTitle"
        "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedTitle"
        "arabseed-tv.com" -> "https://arabseed-tv.com/page/1/?s=$encodedTitle"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
        "stardima.com" -> "https://www.stardima.com/search?query=$encodedTitle&page=1"
        "watch.stardima.com" -> "https://watch.stardima.com/watch/search_gcse-2/?s=$encodedTitle&page=1"
        "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
        "laaroza.space" -> "https://laaroza.space/search.php?keywords=$encodedTitle"
        "witanime.you" -> "https://witanime.you/?search_param=animes&s=$encodedTitle"
        "w1.anime4up.rest" -> "https://w1.anime4up.rest/?search_param=animes&s=$encodedTitle"
        "animeblkom.net" -> "https://animeblkom.net/search?query=$encodedTitle"
        "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
        "arabanime.net" -> "https://www.arabanime.net/?s=$encodedTitle"
        "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
        "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
        else -> "https://$currentSiteName/?s=$encodedTitle"
    }

    if (isLoading && !isFailed) {
        AndroidView(
            modifier = Modifier.size(1.dp).alpha(0.01f),
            factory = { ctx ->
                WebView(ctx).apply {
                    setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        databaseEnabled = true
                        javaScriptCanOpenWindowsAutomatically = true
                        userAgentString = WebSettings.getDefaultUserAgent(ctx)
                        mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                    }
                    val cookieManager = CookieManager.getInstance()
                    cookieManager.setAcceptCookie(true)
                    cookieManager.setAcceptThirdPartyCookies(this, true)
                    
                    addJavascriptInterface(object {
                        private var lastFailedSiteIndex = -1

                        @android.webkit.JavascriptInterface
                        fun sendBypassStatus(status: String) {
                            Handler(Looper.getMainLooper()).post {
                                if (status == "NORMAL" && (bypassStatus == "CHECKING_CLOUDFLARE" || bypassStatus == "CLOUDFLARE")) {
                                    bypassStatus = "VERIFIED"
                                    Handler(Looper.getMainLooper()).postDelayed({
                                        if (bypassStatus == "VERIFIED") bypassStatus = "NORMAL"
                                    }, 1500)
                                } else if (status == "CLOUDFLARE") {
                                    bypassStatus = "CLOUDFLARE"
                                }
                            }
                        }

                        @android.webkit.JavascriptInterface
                        fun sendFailed() {
                            Handler(Looper.getMainLooper()).post {
                                if (lastFailedSiteIndex != currentSiteIndex) {
                                    lastFailedSiteIndex = currentSiteIndex
                                    currentSiteIndex++
                                }
                            }
                        }

                        @android.webkit.JavascriptInterface
                        fun sendServersV2(serversJson: String, url: String) {
                            try {
                                val serversData = org.json.JSONArray(serversJson)
                                val serversNames = mutableListOf<String>()
                                val serversMap = mutableMapOf<String, String>()
                                val serversIds = mutableMapOf<String, String>()
                                
                                for (i in 0 until serversData.length()) {
                                    val item = serversData.getJSONObject(i)
                                    val name = item.getString("name")
                                    val link = if (item.has("link")) item.getString("link") else ""
                                    val id = if (item.has("id")) item.getString("id") else ""
                                    serversNames.add(name)
                                    serversMap[name] = link
                                    serversIds[name] = id
                                }
                                
                                if (serversNames.isNotEmpty() && extractedServers.isEmpty()) {
                                    Handler(Looper.getMainLooper()).post {
                                        finalWatchUrl = url
                                        extractedServers = serversNames
                                        extractedServerLinks = serversMap
                                        com.example.ui.screens.player.ServerStateStore.extractedServers = serversNames
                                        com.example.ui.screens.player.ServerStateStore.extractedServerLinks = serversMap
                                        com.example.ui.screens.player.ServerStateStore.extractedServerIds = serversIds
                                        isLoading = false
                                    }
                                }
                            } catch (e: Exception) { e.printStackTrace() }
                        }
                        
                        @android.webkit.JavascriptInterface
                        fun sendServers(serversStr: String, url: String) {
                            val servers = serversStr.split(",").filter { it.isNotBlank() }.distinct()
                            if (servers.isNotEmpty() && extractedServers.isEmpty()) {
                                Handler(Looper.getMainLooper()).post {
                                    finalWatchUrl = url
                                    extractedServers = servers
                                    val tempMap = servers.associateWith { "" }
                                    com.example.ui.screens.player.ServerStateStore.extractedServers = servers
                                    com.example.ui.screens.player.ServerStateStore.extractedServerLinks = tempMap
                                    extractedServerLinks = tempMap
                                    isLoading = false
                                    
                                    
                                }
                            }
                        }
                    }, "AndroidBridge")

                    webViewClient = object : WebViewClient() {
                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }

                        override fun onPageFinished(view: WebView, url: String) {
                            super.onPageFinished(view, url)
                            
                            val isMovieStr = if (isMovie) "true" else "false"
                            val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode)
                            view.evaluateJavascript(autoPlayScript, null)
                        }
                    }
                }
            },
            update = { webView ->
                val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String
                if (lastUrl != searchUrl) {
                    webView.setTag(com.example.R.id.tag_url, searchUrl)
                    webView.loadUrl(searchUrl)
                }
            }
        )
    }

Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        val isVerified = bypassStatus == "VERIFIED"
        val isNormal = bypassStatus == "NORMAL"
        val isCloudflare = bypassStatus == "CLOUDFLARE" || bypassStatus == "CHECKING_CLOUDFLARE"

        val activeColor = if (isVerified || isNormal) Color(0xFF00C853) else Color(0xFFFF1111)

        Box(
            modifier = Modifier
                .fillMaxWidth(0.95f)
                .wrapContentHeight()
                .clip(RoundedCornerShape(24.dp))
                .background(Color(0xFF16161A))
                .border(1.dp, Color(0x33FF1111), RoundedCornerShape(24.dp))
        ) {
            // Subtle top-left / top-right radial gradient for the red glow
            Box(
                modifier = Modifier
                    .matchParentSize()
                    .background(
                        Brush.radialGradient(
                            colors = listOf(Color(0x15FF1111), Color.Transparent),
                            radius = 600f,
                            center = androidx.compose.ui.geometry.Offset(0f, 0f)
                        )
                    )
            )

            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .background(Color(0xFF330000), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = androidx.compose.material.icons.Icons.Outlined.CloudDownload,
                                contentDescription = null,
                                tint = Color.White,
                                modifier = Modifier.size(24.dp)
                            )
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column {
                            Text(
                                text = "اختر السيرفر",
                                color = Color.White,
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = "جاري الإتصال بالسيرفرات المتاحة...",
                                color = Color.Gray,
                                style = MaterialTheme.typography.bodySmall
                            )
                        }
                    }

                    IconButton(
                        onClick = onDismiss,
                        modifier = Modifier
                            .size(36.dp)
                            .background(Color(0xFF222225), CircleShape)
                            .border(1.dp, Color(0xFF333333), CircleShape)
                    ) {
                        Icon(Icons.Default.Close, contentDescription = "إغلاق", tint = Color.White, modifier = Modifier.size(18.dp))
                    }
                }

                Spacer(modifier = Modifier.height(32.dp))

                if (isLoading) {
                    // Loading State matching design
                    Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier.size(140.dp)
                    ) {
                        // Faint outer rings
                        androidx.compose.foundation.Canvas(modifier = Modifier.size(140.dp)) {
                            drawCircle(
                                color = Color(0x15FF1111),
                                radius = size.minDimension / 2,
                                style = androidx.compose.ui.graphics.drawscope.Stroke(width = 1.dp.toPx())
                            )
                            drawCircle(
                                color = Color(0x25FF1111),
                                radius = size.minDimension / 2 - 20f,
                                style = androidx.compose.ui.graphics.drawscope.Stroke(width = 1.dp.toPx())
                            )
                        }
                        
                        CircularProgressIndicator(
                            color = activeColor,
                            trackColor = Color(0xFF222225),
                            modifier = Modifier.size(90.dp),
                            strokeWidth = 6.dp
                        )
                    }

                    Spacer(modifier = Modifier.height(32.dp))

                    val statusMsg = if (isVerified) {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("عملية تحديث البيانات ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append("نجحت!") }
                        }
                    } else if (isNormal) {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري الفحص في ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                        }
                    } else {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري عملية ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFFFF1111))) { append("تحديث البيانات...") }
                        }
                    }

                    Text(
                        text = statusMsg,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = "الرجاء الإنتظار، يتم جلب أحدث المعلومات من السيرفرات.",
                        color = Color.Gray,
                        style = MaterialTheme.typography.bodySmall,
                        textAlign = TextAlign.Center
                    )

                    Spacer(modifier = Modifier.height(32.dp))

                    // Badges Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceEvenly,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        StatusBadge(
                            text = "جاري التحقق",
                            icon = androidx.compose.material.icons.Icons.Outlined.Storage,
                            statusColor = activeColor
                        )
                        StatusBadge(
                            text = "تحديث البيانات",
                            icon = androidx.compose.material.icons.Icons.Outlined.Sync,
                            statusColor = activeColor
                        )
                        StatusBadge(
                            text = "اتصال آمن",
                            icon = androidx.compose.material.icons.Icons.Outlined.Security,
                            statusColor = if (isVerified || isNormal) Color(0xFF00C853) else Color.Gray
                        )
                    }

                    Spacer(modifier = Modifier.height(24.dp))

                    // Bottom progress line
                    val progress = (currentSiteIndex.toFloat() / prioritySites.size.coerceAtLeast(1).toFloat()).coerceIn(0f, 1f)
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(4.dp)
                            .clip(RoundedCornerShape(2.dp))
                            .background(Color(0xFF222225))
                    ) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth(if (progress == 0f) 0.1f else progress)
                                .height(4.dp)
                                .background(activeColor)
                        )
                    }

                } else if (isFailed) {
                    Text(
                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                        color = Color(0xFFFF1111),
                        style = MaterialTheme.typography.bodyLarge,
                        textAlign = TextAlign.Center
                    )
                } else if (extractedServers.isNotEmpty()) {
                    Text(
                        text = "تم جلب السيرفرات من: $currentSiteName",
                        color = Color(0xFF00C853),
                        style = MaterialTheme.typography.labelLarge,
                        modifier = Modifier.padding(bottom = 16.dp)
                    )
                    
                    LazyColumn(
                        modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(extractedServers) { server ->
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        onPlay(extractedServerLinks[server] ?: finalWatchUrl ?: searchUrl, server, currentSiteName)
                                    },
                                colors = CardDefaults.cardColors(
                                    containerColor = Color(0xFF222225)
                                ),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(16.dp),
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.Center
                                ) {
                                    Text(
                                        text = server,
                                        color = Color.White,
                                        style = MaterialTheme.typography.titleMedium,
                                        fontWeight = FontWeight.Bold
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF19191C))
            .border(1.dp, Color(0xFF2C2C2E), RoundedCornerShape(16.dp))
            .padding(horizontal = 10.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
        Spacer(modifier = Modifier.width(6.dp))
        Text(text, color = Color.LightGray, fontSize = 11.sp)
        Spacer(modifier = Modifier.width(6.dp))
        Box(modifier = Modifier.size(6.dp).background(statusColor, CircleShape))
    }
}