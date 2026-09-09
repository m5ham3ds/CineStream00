package com.example.extensions.providers

import com.example.extensions.ProviderExtension
import com.example.ui.screens.player.SiteScripts
import java.net.URLEncoder

class LegacySiteExtension(
    override val id: String,
    override val name: String,
    override val baseUrl: String,
    override val isAnime: Boolean,
    override val isMovie: Boolean,
    override val isSeries: Boolean
) : ProviderExtension {
    override val lang = "ar"
    override val iconUrl = ""

    override fun getSearchUrl(titleOriginal: String, titleClean: String): String {
        val encodedOriginal = URLEncoder.encode(titleOriginal, "UTF-8")
        val encodedPlusOriginal = URLEncoder.encode(titleOriginal, "UTF-8").replace("%20", "+")
        val encodedClean = URLEncoder.encode(titleClean, "UTF-8")
        val encodedPlusClean = URLEncoder.encode(titleClean, "UTF-8").replace("%20", "+")

        return when (name) {
            "w1.anime4up.rest" -> "https://w1.anime4up.rest/?s=$encodedOriginal"
            "animeblkom.net" -> "https://animeblkom.net/search?query=$encodedPlusOriginal"
            "animeat.net" -> "https://animeat.net/"
            "arabanime.net" -> "https://www.arabanime.net/searchq"
            "det.animerco.org" -> "https://det.animerco.org/?s=$encodedPlusOriginal"
            "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedPlusOriginal"
            "tv10.egydead.live" -> "https://tv10.egydead.live/?s=$encodedPlusOriginal"
            "a.qfilm.tv" -> "https://a.qfilm.tv/search.php?keywords=$encodedPlusOriginal&video-id=#"
            "egybests.live" -> "http://egybests.live/?s=$encodedPlusOriginal"
            "arabseed.wine" -> "https://www.arabseed.wine/?s=$encodedPlusOriginal&type="
            "topcinema.io" -> "https://topcinema.io/"
            "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedPlusOriginal&video-id="
            "arabseed-tv.com" -> "https://arabseed-tv.com/"
            "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedPlusOriginal&video-id=#"
            "stardima.com", "watch.stardima.com" -> "https://www.stardima.com/search?query=$encodedOriginal"
            "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedPlusOriginal&video-id="
            "laaroza.space" -> "https://laaroza.sbs/search.php?keywords=$encodedPlusOriginal"
            else -> "https://$name/?s=$encodedPlusOriginal"
        }
    }

    override fun getExtractionScript(isMovie: Boolean, episode: Int, title: String): String {
        return SiteScripts.getScriptForSite(name, isMovie, episode, title)
    }
}
