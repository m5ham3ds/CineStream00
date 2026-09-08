import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_code = """                                        // CLEAR PREVIOUS SESSION DATA TO FORCE RE-VERIFICATION
                                        android.webkit.WebStorage.getInstance().deleteAllData()
                                        android.webkit.CookieManager.getInstance().removeAllCookies(null)
                                        android.webkit.CookieManager.getInstance().flush()"""

new_code = """                                        // ENABLE COOKIES AND DOM STORAGE FOR PERSISTENCE
                                        android.webkit.CookieManager.getInstance().setAcceptCookie(true)
                                        android.webkit.CookieManager.getInstance().setAcceptThirdPartyCookies(this, true)"""

content = content.replace(old_code, new_code)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)

