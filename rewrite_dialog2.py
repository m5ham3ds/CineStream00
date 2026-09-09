import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

start_str = "if (isLoading && !isFailed) {"
end_str = "} // End if (!isCloudflare)"

start_idx = content.find(start_str)
end_idx = content.find(end_str) + len(end_str)

if start_idx != -1 and end_idx != -1:
    original_block = content[start_idx:end_idx]
    
    # Extract AndroidView factory
    factory_start = original_block.find("factory = { ctx ->")
    factory_end = original_block.find("update = { view ->")
    if factory_end == -1:
        factory_end = original_block.find("} // End AndroidView Box")
    
    # We will replace the entire original_block with our new layout
    new_block = """if (isLoading && !isFailed) {
                    androidx.compose.animation.AnimatedContent(
                        targetState = bypassStatus,
                        transitionSpec = {
                            androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) androidx.compose.animation.togetherWith androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300))
                        }, label = "BypassAnimation"
                    ) { currentStatus ->
                        Box(
                            modifier = Modifier.fillMaxWidth().height(450.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp)),
                            contentAlignment = Alignment.Center
                        ) {
                            // 1. The WebView (Always present, but hidden by overlay if not Cloudflare)
                            key(retryTrigger) {
                                AndroidView(
                                    modifier = Modifier.fillMaxSize().alpha(if (currentStatus == "CLOUDFLARE") 1f else 0.01f),
                                    factory = { ctx ->
                                        WebView(ctx).apply {
                                            android.webkit.CookieManager.getInstance().setAcceptCookie(true)
                                            android.webkit.CookieManager.getInstance().setAcceptThirdPartyCookies(this, true)
                                            setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                                            settings.apply {
                                                javaScriptEnabled = true
                                                domStorageEnabled = true
                                                databaseEnabled = true
                                                javaScriptCanOpenWindowsAutomatically = true
                                                userAgentString = "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36"
                                                mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                                            }
                                            val cookieManager = android.webkit.CookieManager.getInstance()
                                            cookieManager.setAcceptCookie(true)
                                            cookieManager.setAcceptThirdPartyCookies(this, true)
                                            
                                            addJavascriptInterface(object {
                                                private var lastFailedSiteIndex = -1
                                                @android.webkit.JavascriptInterface
                                                fun logDebug(msg: String) {
                                                    android.util.Log.d("AISTUDIO_DEBUG", msg)
                                                }
                                                @android.webkit.JavascriptInterface
                                                fun sendBypassStatus(status: String) {
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                        if (status == "NORMAL" && (bypassStatus == "CHECKING_CLOUDFLARE" || bypassStatus == "CLOUDFLARE")) {
                                                            android.webkit.CookieManager.getInstance().flush()
                                                            bypassStatus = "VERIFIED"
                                                            android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                                                                if (bypassStatus == "VERIFIED") bypassStatus = "NORMAL"
                                                            }, 1500)
                                                        } else if (status == "CLOUDFLARE") {
                                                            bypassStatus = "CLOUDFLARE"
                                                        }
                                                    }
                                                }
                                                @android.webkit.JavascriptInterface
                                                fun sendFailed() {
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
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
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
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
                                                        android.os.Handler(android.os.Looper.getMainLooper()).post {
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
                                            
                                            webChromeClient = object : android.webkit.WebChromeClient() {
                                                override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                                    super.onProgressChanged(view, newProgress)
                                                    if (newProgress >= 30) {
                                                        val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                        view?.evaluateJavascript(autoPlayScript, null)
                                                    }
                                                }
                                            }
                                            
                                            webViewClient = object : android.webkit.WebViewClient() {
                                                private var isNotified = false
                                                private var urlToCheck = ""
                                                private var checkAttempt = 0
                                                
                                                override fun onPageStarted(view: WebView?, url: String?, favicon: android.graphics.Bitmap?) {
                                                    super.onPageStarted(view, url, favicon)
                                                    isNotified = false
                                                    checkAttempt = 0
                                                    android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                        if (bypassStatus == "CLOUDFLARE") {
                                                            bypassStatus = "CHECKING_CLOUDFLARE"
                                                        }
                                                    }
                                                }
                                                
                                                override fun onPageFinished(view: WebView?, url: String?) {
                                                    super.onPageFinished(view, url)
                                                    if (url != null) { urlToCheck = url }
                                                    if (!isNotified) { repeatCheck(view, 0) }
                                                }
                                                
                                                private fun repeatCheck(view: WebView?, attempt: Int) {
                                                    if (attempt > 30 || isNotified) return
                                                    
                                                    val checkJS = \"\"\"
                                                        (function() {
                                                            var isCloudflare = document.getElementById('challenge-running') !== null ||
                                                                               document.querySelector('.cf-browser-verification') !== null ||
                                                                               document.querySelector('#cf-wrapper') !== null ||
                                                                               document.querySelector('#turnstile-wrapper') !== null ||
                                                                               document.body.innerHTML.indexOf('cf-turnstile') !== -1 ||
                                                                               document.title.toLowerCase().indexOf('just a moment') !== -1 ||
                                                                               document.title.toLowerCase().indexOf('attention required') !== -1 ||
                                                                               document.body.innerText.indexOf('Checking your browser') !== -1 ||
                                                                               document.body.innerText.indexOf('Verify you are human') !== -1;

                                                            if (isCloudflare) {
                                                                try { AndroidBridge.sendBypassStatus('CLOUDFLARE'); } catch (e) {}
                                                                return false;
                                                            }

                                                            var contentExists = document.querySelector('video') !== null ||
                                                                                document.querySelector('iframe') !== null ||
                                                                                document.querySelector('.download-btn') !== null ||
                                                                                document.getElementById('player-container') !== null ||
                                                                                document.body.innerText.length > 200;
                                                                                
                                                            return contentExists;
                                                        })();
                                                    \"\"\".trimIndent()

                                                    view?.evaluateJavascript(checkJS) { result ->
                                                        if (result == "true" && !isNotified) {
                                                            isNotified = true
                                                            android.os.Handler(android.os.Looper.getMainLooper()).post {
                                                                android.webkit.CookieManager.getInstance().flush()
                                                                bypassStatus = "NORMAL"
                                                            }
                                                            val autoPlayScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)
                                                            view?.evaluateJavascript(autoPlayScript, null)
                                                        } else {
                                                            android.os.Handler(android.os.Looper.getMainLooper()).postDelayed({
                                                                repeatCheck(view, attempt + 1)
                                                            }, 1000)
                                                        }
                                                    }
                                                }
                                            }
                                            
                                            val targetUrl = com.example.ui.screens.player.SiteScripts.getSiteUrl(currentSiteName, isMovie, title, season, episode)
                                            loadUrl(targetUrl)
                                        }
                                    }
                                )
                            }
                            
                            // 2. The Overlay UI (Shown when NOT CLOUDFLARE)
                            if (currentStatus != "CLOUDFLARE") {
                                Box(
                                    modifier = Modifier.fillMaxSize().background(Color(0xFF16161A)),
                                    contentAlignment = Alignment.Center
                                ) {
                                    if (isNetworkError) {
                                        Column(
                                            horizontalAlignment = Alignment.CenterHorizontally,
                                            modifier = Modifier.padding(16.dp)
                                        ) {
                                            Icon(
                                                imageVector = androidx.compose.material.icons.Icons.Default.Close,
                                                contentDescription = "Network Error",
                                                tint = Color(0xFFFF1111),
                                                modifier = Modifier.size(64.dp)
                                            )
                                            Spacer(modifier = Modifier.height(16.dp))
                                            Text(
                                                text = "حدث خطأ في الاتصال بالإنترنت",
                                                color = Color.White,
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold
                                            )
                                            Spacer(modifier = Modifier.height(8.dp))
                                            Text(
                                                text = "يرجى التحقق من الشبكة والمحاولة مرة أخرى.",
                                                color = Color.Gray,
                                                style = MaterialTheme.typography.bodySmall
                                            )
                                            Spacer(modifier = Modifier.height(24.dp))
                                            Button(
                                                onClick = { 
                                                    isNetworkError = false
                                                    retryTrigger++ 
                                                },
                                                colors = androidx.compose.material3.ButtonDefaults.buttonColors(containerColor = activeColor),
                                                shape = RoundedCornerShape(12.dp)
                                            ) {
                                                Text("إعادة المحاولة", color = Color.White, fontWeight = FontWeight.Bold)
                                            }
                                        }
                                    } else {
                                        Column(
                                            horizontalAlignment = Alignment.CenterHorizontally,
                                            modifier = Modifier.padding(16.dp)
                                        ) {
                                            Box(
                                                contentAlignment = Alignment.Center,
                                                modifier = Modifier.size(140.dp)
                                            ) {
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
                                            val statusMsg = when (bypassStatus) {
                                                "CHECKING_CLOUDFLARE" -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تأمين الاتصال بموقع ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                                                    }
                                                }
                                                "CLOUDFLARE" -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تخطي حماية ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFFFF1111))) { append("Cloudflare") }
                                                    }
                                                }
                                                "VERIFIED" -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تم التخطي ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append("بنجاح") }
                                                    }
                                                }
                                                else -> {
                                                    androidx.compose.ui.text.buildAnnotatedString {
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري البحث في ") }
                                                        withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                                                    }
                                                }
                                            }
                                            Text(
                                                text = statusMsg,
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold,
                                                textAlign = TextAlign.Center,
                                                maxLines = 1,
                                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                                                modifier = Modifier.fillMaxWidth()
                                            )
                                            Spacer(modifier = Modifier.height(8.dp))
                                            Text(
                                                text = "الرجاء الإنتظار، يتم جلب أحدث المعلومات من السيرفرات.",
                                                color = Color.Gray,
                                                style = MaterialTheme.typography.bodySmall,
                                                textAlign = TextAlign.Center,
                                                maxLines = 1,
                                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                                                modifier = Modifier.fillMaxWidth()
                                            )
                                            Spacer(modifier = Modifier.height(32.dp))
                                            Row(
                                                modifier = Modifier.fillMaxWidth(),
                                                horizontalArrangement = Arrangement.spacedBy(4.dp, Alignment.CenterHorizontally),
                                                verticalAlignment = Alignment.CenterVertically
                                            ) {
                                                StatusBadge(
                                                    text = "جاري التحقق",
                                                    icon = androidx.compose.material.icons.Icons.Outlined.Storage,
                                                    statusColor = activeColor
                                                )
                                                StatusBadge(
                                                    text = "جلب السيرفرات",
                                                    icon = androidx.compose.material.icons.Icons.Outlined.Sync,
                                                    statusColor = activeColor
                                                )
                                                StatusBadge(
                                                    text = "اتصال آمن",
                                                    icon = androidx.compose.material.icons.Icons.Outlined.Security,
                                                    statusColor = if (bypassStatus == "VERIFIED" || bypassStatus == "NORMAL") Color(0xFF00C853) else Color.Gray
                                                )
                                            }
                                            Spacer(modifier = Modifier.height(24.dp))
                                        }
                                    }
                                }
                            }
                        }
                    } // End AnimatedContent
                    """
    
    content = content[:start_idx] + new_block + content[end_idx:]
    
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
        
    print("Replacement successful")
else:
    print("Block not found!")

