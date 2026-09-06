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
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun HiddenVideoExtractor(
    url: String,
    isMovie: Boolean = true,
    season: Int = 1,
    episode: Int = 1,
    targetServer: String? = null,
    targetServerId: String? = null,
    onVideoUrlFound: (String) -> Unit,
    onIframeUrlFound: ((String) -> Unit)? = null,
    onServersFound: ((List<String>) -> Unit)? = null
) {
    AndroidView(
        modifier = Modifier.size(1.dp).alpha(0f), // Completely invisible but active in layout
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
                    cacheMode = WebSettings.LOAD_DEFAULT
                    // This is critical: force media to auto-play so we can catch the network request
                    mediaPlaybackRequiresUserGesture = false 
                }

                val cookieManager = CookieManager.getInstance()
                cookieManager.setAcceptCookie(true)
                cookieManager.setAcceptThirdPartyCookies(this, true)

                addJavascriptInterface(object {
                    @android.webkit.JavascriptInterface
                    fun sendServers(serversStr: String) {
                        val servers = serversStr.split(",").filter { it.isNotBlank() }
                        if (servers.isNotEmpty()) {
                            Handler(Looper.getMainLooper()).post {
                                onServersFound?.invoke(servers)
                            }
                        }
                    }
                    
                    @android.webkit.JavascriptInterface
                    fun sendIframeUrl(url: String) {
                        Handler(Looper.getMainLooper()).post {
                            onIframeUrlFound?.invoke(url) ?: onVideoUrlFound(url)
                        }
                    }
                }, "AndroidBridge")

                webViewClient = object : WebViewClient() {
                    var found = false

                    override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                        handler?.proceed()
                    }

                    override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                        found = false
                        super.onPageStarted(view, url, favicon)
                    }

                    override fun shouldInterceptRequest(
                        view: WebView?,
                        request: WebResourceRequest?
                    ): WebResourceResponse? {
                        val reqUrl = request?.url.toString()
                        
                        // Look for standard streaming formats
                        if (!found && (reqUrl.contains(".m3u8") || reqUrl.contains(".mp4") || reqUrl.contains(".mkv") || reqUrl.contains("videodelivery.net") || reqUrl.contains("v.mp4"))) {
                            // Avoid common ad scripts that might have these strings
                            if (!reqUrl.contains("adsystem") && !reqUrl.contains("tracker") && !reqUrl.contains("googleads") && !reqUrl.contains("facebook") && !reqUrl.contains("tiktok")) {
                                found = true
                                Handler(Looper.getMainLooper()).post {
                                    onVideoUrlFound(reqUrl)
                                }
                            }
                        }
                        
                        return super.shouldInterceptRequest(view, request)
                    }

                    override fun onPageFinished(view: WebView, url: String) {
                        super.onPageFinished(view, url)
                        // Inject script to automatically click play buttons to force stream load
                        val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForVideoExtractor(url, targetServerId)
                        view.evaluateJavascript(autoPlayScript, null)
                    }
                }
            }
        },
        update = { webView ->
            // Use getTag to store the original loaded url to avoid reloading when webView.url changes due to internal navigation
            val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String
            val lastServer = webView.getTag(com.example.R.id.tag_server) as? String

            if (lastUrl != url) {
                webView.setTag(com.example.R.id.tag_url, url)
                webView.setTag(com.example.R.id.tag_server, targetServer)
                webView.loadUrl(url)
            } else if (lastServer != targetServer) {
                webView.setTag(com.example.R.id.tag_server, targetServer)
                webView.reload() // Server changed, reload the page
            }
        }
    )
}
