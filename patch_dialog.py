import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# 1. Add isNetworkError state
state_import = "    var showCancelConfirmDialog by remember { mutableStateOf(false) }"
if "var isNetworkError" not in content:
    content = content.replace(state_import, state_import + "\n    var isNetworkError by remember { mutableStateOf(false) }")

# 2. Fix AndroidView sizing by wrapping it in a Box
old_android_view = """            AndroidView(
                                modifier = if (isCloudflare) Modifier.fillMaxWidth().height(450.dp) else Modifier.size(1.dp).alpha(0.01f),
                                factory = {"""

new_android_view = """            Box(modifier = if (isCloudflare) Modifier.fillMaxWidth().height(450.dp) else Modifier.size(1.dp).alpha(0f)) {
                            AndroidView(
                                modifier = Modifier.fillMaxSize(),
                                factory = {"""

content = content.replace(old_android_view, new_android_view)

# Add closing brace for the Box
old_android_view_end = """                                    }
                                }
                            )
                        }"""
new_android_view_end = """                                    }
                                }
                            )
                        } // End AndroidView Box
                        }"""
content = content.replace(old_android_view_end, new_android_view_end)

# 3. Handle onReceivedError for network failure
old_webview_client = """                                        webViewClient = object : WebViewClient() {
                                            override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                                                handler?.proceed()
                                            }"""
new_webview_client = """                                        webViewClient = object : WebViewClient() {
                                            override fun onReceivedSslError(view: WebView?, handler: android.webkit.SslErrorHandler?, error: android.net.http.SslError?) {
                                                handler?.proceed()
                                            }
                                            override fun onReceivedError(view: WebView?, request: android.webkit.WebResourceRequest?, error: android.webkit.WebResourceError?) {
                                                super.onReceivedError(view, request, error)
                                                if (request?.isForMainFrame == true) {
                                                    Handler(Looper.getMainLooper()).post {
                                                        isNetworkError = true
                                                    }
                                                }
                                            }"""
content = content.replace(old_webview_client, new_webview_client)

# 4. Show Network Error UI
old_loading_ui = """                    if (!isCloudflare) {
                        // Loading State matching design
                        Box("""

new_loading_ui = """                    if (isNetworkError) {
                        Column(
                            modifier = Modifier.fillMaxWidth().padding(vertical = 32.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Icon(
                                imageVector = androidx.compose.material.icons.Icons.Default.Warning,
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
                                colors = ButtonDefaults.buttonColors(containerColor = activeColor),
                                shape = RoundedCornerShape(12.dp)
                            ) {
                                Text("إعادة المحاولة", color = Color.White, fontWeight = FontWeight.Bold)
                            }
                        }
                    } else if (!isCloudflare) {
                        // Loading State matching design
                        Box("""
content = content.replace(old_loading_ui, new_loading_ui)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
print("ServerSelectionDialog patched!")
