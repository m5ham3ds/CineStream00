package com.example.ui.screens.player

import android.annotation.SuppressLint
import android.os.Handler
import android.os.Looper
import android.webkit.CookieManager
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import kotlinx.coroutines.delay

@SuppressLint("SetJavaScriptEnabled")
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
    val priorityAnimeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "Animerco", "AnimeLuxe", "Stardima", "Watch Stardima")
    val priorityMovieSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "Laaroza", "Almeshkah", "ArabSeed Wine", "ArabSeed", "Egy Best", "CimaLight", "Brstej")
    val prioritySeriesSites = listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine", "Almeshkah", "Laaroza", "QFilm", "ArabSeed", "CimaLight", "Brstej")

    val prioritySites = if (isAnime) priorityAnimeSites else if (isMovie) priorityMovieSites else prioritySeriesSites

    var currentSiteIndex by remember { mutableStateOf(0) }
    var currentSiteName by remember { mutableStateOf(prioritySites[0]) }
    
    var isLoading by remember { mutableStateOf(true) }
    var loadingMessage by remember { mutableStateOf("جاري البحث...") }
    var isFailed by remember { mutableStateOf(false) }

    var watchUrlToLoad by remember { mutableStateOf<String?>(null) }
    var foundVideoUrl by remember { mutableStateOf(false) }

    val tryNextSite: () -> Unit = {
        if (currentSiteIndex < prioritySites.size - 1) {
            currentSiteIndex++
            currentSiteName = prioritySites[currentSiteIndex]
            watchUrlToLoad = null
            foundVideoUrl = false
        } else {
            isLoading = false
            isFailed = true
        }
    }

    LaunchedEffect(currentSiteIndex) {
        isLoading = true
        loadingMessage = "البحث في موقع $currentSiteName..."
        watchUrlToLoad = null
        foundVideoUrl = false

        var directUrl: String? = null
        try {
            directUrl = com.example.data.repository.ScraperRepository.getWatchUrl(currentSiteName, title, isMovie, season, episode)
        } catch (e: Exception) {}

        if (directUrl != null) {
            watchUrlToLoad = directUrl
        } else {
            val encodedTitle = java.net.URLEncoder.encode(title, "UTF-8")
            val domain = when (currentSiteName) {
                "WitAnime" -> "witanime.cyou"
                "Anime4up" -> "w1.anime4up.rest"
                "AnimeBlkom" -> "animeblkom.net"
                "Animeat" -> "animeat.net"
                "Arabanime" -> "arabanime.net"
                "Animerco" -> "det.animerco.org"
                "AnimeLuxe" -> "vip.animeluxe.org"
                "Stardima" -> "stardima.com"
                "Watch Stardima" -> "watch.stardima.com"
                "EgyDead TV10" -> "tv10.egydead.live"
                "QFilm" -> "a.qfilm.tv"
                "TopCinema" -> "topcinema.io"
                "Laaroza" -> "laaroza.space"
                "Almeshkah" -> "z1.almeshkah.net"
                "ArabSeed Wine" -> "arabseed.wine"
                "ArabSeed" -> "arabseed-tv.com"
                "Egy Best" -> "egybests.live"
                "CimaLight" -> "e.cimalight.co"
                "Brstej" -> "uo.brstej.com"
                else -> currentSiteName
            }
            watchUrlToLoad = when {
                domain.contains("egydead") -> "https://$domain/page/1/?s=$encodedTitle"
                domain.contains("qfilm") -> "https://$domain/search.php?keywords=$encodedTitle"
                domain.contains("arabseed") -> "https://$domain/page/1/?s=$encodedTitle"
                domain.contains("stardima") -> "https://$domain/search?query=$encodedTitle&page=1"
                domain.contains("witanime") -> "https://$domain/?search_param=animes&s=$encodedTitle"
                domain.contains("anime4up") -> "https://$domain/?search_param=animes&s=$encodedTitle"
                domain.contains("cima4u") -> "https://$domain/search.php?keywords=$encodedTitle"
                domain.contains("faselhd") -> "https://$domain/?s=$encodedTitle"
                domain == "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
                domain == "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
                domain == "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
                domain == "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
                domain == "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
                domain == "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
                else -> "https://$domain/?s=$encodedTitle"
            }
        }
    }

    if (isLoading && !isFailed && watchUrlToLoad != null) {
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
                        mediaPlaybackRequiresUserGesture = false
                    }
                    val cookieManager = CookieManager.getInstance()
                    cookieManager.setAcceptCookie(true)
                    cookieManager.setAcceptThirdPartyCookies(this, true)

                    addJavascriptInterface(object {
                        @android.webkit.JavascriptInterface
                        fun sendFailed() {
                            Handler(Looper.getMainLooper()).post {
                                tryNextSite()
                            }
                        }
                    }, "AndroidBridge")

                    webViewClient = object : WebViewClient() {
                        override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                            handler?.proceed()
                        }
                        
                        override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest?): WebResourceResponse? {
                            val reqUrl = request?.url.toString()
                            if (!foundVideoUrl && (reqUrl.contains(".m3u8") || reqUrl.contains(".mp4") || reqUrl.contains(".mkv") || reqUrl.contains("videodelivery.net") || reqUrl.contains("v.mp4"))) {
                                if (!reqUrl.contains("adsystem") && !reqUrl.contains("tracker") && !reqUrl.contains("googleads") && !reqUrl.contains("facebook") && !reqUrl.contains("tiktok")) {
                                    foundVideoUrl = true
                                    Handler(Looper.getMainLooper()).post {
                                        onPlay(reqUrl, "Direct", currentSiteName)
                                    }
                                }
                            }
                            return super.shouldInterceptRequest(view, request)
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
                                        var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                        if (cf) { cf.click(); return; }
                                        try {
                                            var iframesCF = document.querySelectorAll('iframe');
                                            for (var i = 0; i < iframesCF.length; i++) {
                                                try {
                                                    var innerBtn = iframesCF[i].contentWindow.document.querySelector('input[type="checkbox"]');
                                                    if (innerBtn) innerBtn.click();
                                                } catch (err) {}
                                            }
                                        } catch(e) {}
                                        var isCloudflare = cf || document.body.innerHTML.includes('Just a moment');

                                        if (loc.includes('?s=') || loc.includes('&s=') || loc.includes('search') || loc.includes('query=')) {
                                            var results = document.querySelectorAll('a.postBlock, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a,  ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0, .pm-ul-browse-videos li a, div.as-episode a, div.Small--Box a, div.anime-card-container a, div.anime-card-poster a');
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
                                                if (targetResult.href && targetResult.href.includes('javascript:void(0)')) { targetResult.click(); } else { window.location.href = targetResult.href; }
                                                return;
                                            }
                                        }
                                        
                                        var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button, ul.servers__list li, div.embeding ul li, ul#watch-servers-list li, button.watchButton, div.servers span.server a, div.watch--servers--list li.server--item, ul.WatchServers li, ul.list_servers li');
                                        var hasServers = serverList && serverList.length > 0;
                                        
                                        var playBtn = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .play-icon, #play-video, .btn-play');
                                        if (playBtn) playBtn.click();
                                        
                                        var watchNowBtn = document.querySelector('.watchNow button, .watchNow form button, .watch-btn, #watch-btn');
                                        if (watchNowBtn && !hasServers && document.querySelectorAll('iframe').length === 0 && document.querySelectorAll('video').length === 0) {
                                            watchNowBtn.click();
                                            return;
                                        }
                                        
                                        var videoTags = document.querySelectorAll('video');
                                        var hasVideo = videoTags.length > 0;

                                        if (!isMovie && !hasServers && document.querySelectorAll('iframe').length === 0 && !hasVideo) {
                                            var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a, div#eps a.list-group-item, ul.episodes__blocks__holder a, div.SeasonsEpisodesMain div.tabcontent a, div.row a, div.all-episodes a, ul#episodes-list-container a, ul.episodes-lists a, ul.episodes-links a, div.episodes-card-title a, div.episodes-card-container a');
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
                                                    if (targetEp.href && targetEp.href.includes('javascript:void(0)')) { targetEp.click(); } else { window.location.href = targetEp.href; }
                                                } else {
                                                    for(var i=0; i<epLinks.length; i++) {
                                                        if((epLinks[i].innerText || "").includes(epNum.toString())) {
                                                            targetEp = epLinks[i]; break;
                                                        }
                                                    }
                                                    var finalTarget = targetEp ? targetEp : epLinks[0];
                                                    if (finalTarget.href && finalTarget.href.includes('javascript:void(0)')) { finalTarget.click(); } else { window.location.href = finalTarget.href; }
                                                }
                                                return;
                                            }
                                        }
                                        
                                        if (hasServers) {
                                            serverList[0].click(); // Click first server to auto-play it!
                                        } else if (document.querySelectorAll('iframe').length > 0) {
                                            var iframes = document.querySelectorAll('iframe');
                                            for(var i=0; i<iframes.length; i++) {
                                                try {
                                                    var innerBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video');
                                                    if(innerBtn) innerBtn.click();
                                                } catch(e) {}
                                            }
                                        }
                                        
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
                if (watchUrlToLoad != null && lastUrl != watchUrlToLoad) {
                    webView.setTag(com.example.R.id.tag_url, watchUrlToLoad)
                    webView.loadUrl(watchUrlToLoad!!)
                }
            }
        )
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false, dismissOnBackPress = true, dismissOnClickOutside = false)
    ) {
        Surface(
            modifier = Modifier.fillMaxWidth(0.9f).wrapContentHeight(),
            shape = MaterialTheme.shapes.large,
            color = MaterialTheme.colorScheme.surface
        ) {
            Column(
                modifier = Modifier.fillMaxWidth().padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        text = "جاري تحضير الفيديو",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "إغلاق")
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
                if (isLoading) {
                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(text = loadingMessage, color = MaterialTheme.colorScheme.onSurfaceVariant)
                } else if (isFailed) {
                    Text(
                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                        color = MaterialTheme.colorScheme.error,
                        style = MaterialTheme.typography.bodyLarge
                    )
                }
            }
        }
    }
}
