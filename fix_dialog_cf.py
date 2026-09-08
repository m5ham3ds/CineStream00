import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Fix Modifier
old_modifier = """                                modifier = if (bypassStatus == "CLOUDFLARE" || bypassStatus == "CHECKING_CLOUDFLARE") 
                                    Modifier.width(320.dp).height(150.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp)).alpha(if (bypassStatus == "CLOUDFLARE") 1f else 0.01f)
                                else 
                                    Modifier.size(1.dp).alpha(0f),"""

new_modifier = """                                modifier = if (bypassStatus == "CLOUDFLARE" || bypassStatus == "CHECKING_CLOUDFLARE") 
                                    Modifier.fillMaxWidth().height(450.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp))
                                else 
                                    Modifier.size(1.dp).alpha(0f),"""

content = content.replace(old_modifier, new_modifier)

# Fix JS Interface to flush cookies when NORMAL
old_send_status = """                                            @android.webkit.JavascriptInterface
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
                                            }"""

new_send_status = """                                            @android.webkit.JavascriptInterface
                                            fun sendBypassStatus(status: String) {
                                                Handler(Looper.getMainLooper()).post {
                                                    if (status == "NORMAL" && (bypassStatus == "CHECKING_CLOUDFLARE" || bypassStatus == "CLOUDFLARE")) {
                                                        android.webkit.CookieManager.getInstance().flush()
                                                        bypassStatus = "VERIFIED"
                                                        Handler(Looper.getMainLooper()).postDelayed({
                                                            if (bypassStatus == "VERIFIED") bypassStatus = "NORMAL"
                                                        }, 1500)
                                                    } else if (status == "CLOUDFLARE") {
                                                        bypassStatus = "CLOUDFLARE"
                                                    }
                                                }
                                            }"""

content = content.replace(old_send_status, new_send_status)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
