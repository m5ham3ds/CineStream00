import com.darkryh.cloudflare_bypass.BypassClient
open class MyBypassClient : BypassClient() {
    override fun onPageFinished(view: android.webkit.WebView?, url: String?) {
        super.onPageFinished(view, url)
    }
}
