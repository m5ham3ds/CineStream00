import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Clear cookies and local storage when opening the webview
old_webview = """                                    WebView(ctx).apply {
                                        setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                                        settings.apply {"""

new_webview = """                                    WebView(ctx).apply {
                                        // CLEAR PREVIOUS SESSION DATA TO FORCE RE-VERIFICATION
                                        android.webkit.WebStorage.getInstance().deleteAllData()
                                        android.webkit.CookieManager.getInstance().removeAllCookies(null)
                                        android.webkit.CookieManager.getInstance().flush()
                                        
                                        setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                                        settings.apply {"""

content = content.replace(old_webview, new_webview)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)

print("Session clearing logic added.")
