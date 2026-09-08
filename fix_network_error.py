import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_err = """                                            override fun onReceivedError(view: WebView?, request: android.webkit.WebResourceRequest?, error: android.webkit.WebResourceError?) {
                                                super.onReceivedError(view, request, error)
                                                if (request?.isForMainFrame == true) {
                                                    Handler(Looper.getMainLooper()).post {
                                                        isNetworkError = true
                                                    }
                                                }
                                            }"""

new_err = """                                            override fun onReceivedError(view: WebView?, request: android.webkit.WebResourceRequest?, error: android.webkit.WebResourceError?) {
                                                super.onReceivedError(view, request, error)
                                                if (request?.isForMainFrame == true) {
                                                    val errorCode = error?.errorCode ?: 0
                                                    // Only trigger network error UI for actual connectivity issues
                                                    if (errorCode == android.webkit.WebViewClient.ERROR_HOST_LOOKUP || 
                                                        errorCode == android.webkit.WebViewClient.ERROR_CONNECT || 
                                                        errorCode == android.webkit.WebViewClient.ERROR_TIMEOUT) {
                                                        Handler(Looper.getMainLooper()).post {
                                                            isNetworkError = true
                                                        }
                                                    }
                                                }
                                            }"""

content = content.replace(old_err, new_err)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
