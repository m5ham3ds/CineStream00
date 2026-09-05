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
    
    val priorityAnimeSites = listOf("witanime.cyou", "w1.anime4up.rest", "animeblkom.net", "animeat.net", "arabanime.net", "det.animerco.org", "vip.animeluxe.org", "stardima.com", "watch.stardima.com")
    val priorityMovieSites = listOf("tv10.egydead.live", "a.qfilm.tv", "topcinema.io", "laaroza.space", "z1.almeshkah.net", "arabseed.wine", "arabseed-tv.com", "egybests.live", "e.cimalight.co", "uo.brstej.com")
    val prioritySeriesSites = listOf("topcinema.io", "tv10.egydead.live", "egybests.live", "arabseed.wine", "z1.almeshkah.net", "laaroza.space", "a.qfilm.tv", "arabseed-tv.com", "e.cimalight.co", "uo.brstej.com")

    val prioritySites = if (isAnime) priorityAnimeSites else if (isMovie) priorityMovieSites else prioritySeriesSites

    var currentSiteIndex by remember { mutableStateOf(0) }
    var currentSiteName by remember { mutableStateOf(prioritySites[0]) }
    
    var isLoading by remember { mutableStateOf(true) }
    var loadingMessage by remember { mutableStateOf("جاري الفحص وتخطي الحماية...") }
    
    var extractedServers by remember { mutableStateOf<List<String>>(emptyList()) }
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
        
        // 25 seconds timeout per site to account for Cloudflare
        delay(25000)
        if (extractedServers.isEmpty()) {
            currentSiteIndex++
        }
    }

    val encodedTitle = URLEncoder.encode(title, "UTF-8")
    val searchUrl = when {
        currentSiteName.contains("egydead") -> "https://$currentSiteName/?s=$encodedTitle"
        currentSiteName.contains("qfilm") -> "https://$currentSiteName/search.php?keywords=$encodedTitle"
        currentSiteName.contains("arabseed") -> "https://$currentSiteName/?s=$encodedTitle"
        currentSiteName.contains("stardima") -> "https://$currentSiteName/search?query=$encodedTitle&page=1"
        currentSiteName.contains("witanime") -> "https://$currentSiteName/?search_param=animes&s=$encodedTitle"
        currentSiteName.contains("anime4up") -> "https://$currentSiteName/?search_param=animes&s=$encodedTitle"
        currentSiteName.contains("cima4u") -> "https://$currentSiteName/search.php?keywords=$encodedTitle"
        currentSiteName.contains("faselhd") -> "https://$currentSiteName/?s=$encodedTitle"
        currentSiteName == "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
        currentSiteName == "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
        currentSiteName == "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
        currentSiteName == "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
        currentSiteName == "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
        currentSiteName == "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
        currentSiteName == "topcinema.io" -> "https://topcinema.io/?s=$encodedTitle"
        currentSiteName == "laaroza.space" -> "https://laaroza.space/?s=$encodedTitle"
        currentSiteName == "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedTitle"
        currentSiteName == "animeblkom.net" -> "https://animeblkom.net/search?query=$encodedTitle"
        currentSiteName == "arabanime.net" -> "https://www.arabanime.net/?s=$encodedTitle"
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
                        fun sendServers(serversStr: String, url: String) {
                            val servers = serversStr.split(",").filter { it.isNotBlank() }.distinct()
                            if (servers.isNotEmpty() && extractedServers.isEmpty()) {
                                Handler(Looper.getMainLooper()).post {
                                    finalWatchUrl = url
                                    extractedServers = servers
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
                            val autoPlayScript = """
                                (function() {
                                    var isMovie = $isMovieStr;
                                    var season = $season;
                                    var epNum = $episode;
                                    var loc = window.location.href.toLowerCase();
                                    
                                    var intervalId = setInterval(function() {
                                        // Bypass Cloudflare
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        var isJustAMoment = document.title.includes('Just a moment') || document.title.includes('Cloudflare') || document.title.includes('Attention Required');
                                        var isCloudflare = cf || isJustAMoment;
                                        
                                        if (isCloudflare) {
                                            if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("CLOUDFLARE");
                                            if (cf) cf.click();
                                            return;
                                        } else {
                                            if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendBypassStatus("NORMAL");
                                        }

                                        // 1. Search Results -> Click item
                                        if (loc.includes('?s=') || loc.includes('search') || loc.includes('query=')) {
                                            var results = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a,  ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0');
                                            if (results && results.length > 0) {
                                                clearInterval(intervalId);
                                                var targetResult = results[0];
                                                if (!isMovie) {
                                                    var e = epNum.toString();
                                                    for (var i=0; i<results.length; i++) {
                                                        var txt = decodeURIComponent(results[i].href || "").toLowerCase() + " " + (results[i].innerText || results[i].title || results[i].getAttribute('title') || "").toLowerCase();
                                                        if (txt.includes('حلقة ' + e) || txt.includes('حلقه ' + e) || txt.includes('-' + e + '-') || txt.includes('ep ' + e) || txt.includes('episode ' + e) || txt.includes(' ' + e + ' ')) {
                                                            targetResult = results[i];
                                                            break;
                                                        }
                                                    }
                                                }
                                                window.location.href = targetResult.href;
                                                return;
                                            }
                                        }
                                        
                                        // 2. Series Page -> Click Season/Episode
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button');
                                        var hasServers = serverList && serverList.length > 0;
                                        
                                        // Click play buttons or watch forms to reveal iframe if hidden
                                        var playBtn = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .play-icon, #play-video, .btn-play');
                                        if (playBtn) playBtn.click();
                                        
                                        var watchNowBtn = document.querySelector('.watchNow button, .watchNow form button, .watch-btn, #watch-btn');
                                        if (watchNowBtn && !hasServers && !hasIframe && !hasVideo) {
                                            watchNowBtn.click();
                                            return;
                                        }
                                        
                                        var iframes = document.querySelectorAll('iframe');
                                        var hasIframe = false;
                                        for(var i=0; i<iframes.length; i++) {
                                            if(iframes[i].src && !iframes[i].src.includes('cloudflare') && !iframes[i].src.includes('facebook') && !iframes[i].src.includes('twitter')) {
                                                hasIframe = true; break;
                                            }
                                        }

                                        var videoTags = document.querySelectorAll('video');
                                        var hasVideo = videoTags.length > 0;

                                        if (!isMovie && !hasServers && !hasIframe && !hasVideo) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a');
                                            if (epLinks.length > 0) {
                                                clearInterval(intervalId);
                                                var targetEp = null;
                                                for(var i=0; i<epLinks.length; i++) {
                                                    var text = epLinks[i].innerText || "";
                                                    if(text.trim() === epNum.toString() || text.includes(" " + epNum.toString() + " ") || text.includes("حلقة " + epNum) || text.includes("الحلقة " + epNum)) {
                                                        targetEp = epLinks[i];
                                                        break;
                                                    }
                                                }
                                                if(targetEp) {
                                                    window.location.href = targetEp.href;
                                                } else {
                                                    for(var i=0; i<epLinks.length; i++) {
                                                        if((epLinks[i].innerText || "").includes(epNum.toString())) {
                                                            targetEp = epLinks[i]; break;
                                                        }
                                                    }
                                                    window.location.href = targetEp ? targetEp.href : epLinks[0].href;
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 3. Extract Servers on Watch Page
                                        if (hasServers || hasIframe || hasVideo) {
                                            var serverNames = [];
                                            if (hasServers) {
                                                for(var i=0; i<serverList.length; i++) {
                                                    var serverName = serverList[i].innerText.trim();
                                                    if (serverName) {
                                                        var sName = serverName.replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                        if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                            sName = "سيرفر " + (i+1);
                                                        }
                                                        serverNames.push(sName);
                                                    }
                                                }
                                            }
                                            if (serverNames.length === 0 && (hasIframe || hasVideo)) {
                                                serverNames.push("السيرفر الرئيسي");
                                            }
                                            
                                            if (serverNames.length > 0) {
                                                // Make unique
                                                var uniqueServers = [...new Set(serverNames)];
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') {
                                                    AndroidBridge.sendServers(uniqueServers.join(','), window.location.href);
                                                }
                                                return;
                                            }
                                        }
                                        
                                        // 4. Fast Fail (if no search results or servers found after loading)
                                        if (!isCloudflare && document.readyState === 'complete') {
                                            window._failCount = (window._failCount || 0) + 1;
                                            if (window._failCount >= 6) {
                                                clearInterval(intervalId);
                                                if (typeof AndroidBridge !== 'undefined') AndroidBridge.sendFailed();
                                            }
                                        }
                                    }, 1500);
                                })();
                            """.trimIndent()
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
                                        onPlay(finalWatchUrl ?: searchUrl, server, currentSiteName)
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