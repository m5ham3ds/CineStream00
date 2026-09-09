package com.example.extensions.providers

import com.example.extensions.ProviderExtension
import com.example.ui.screens.player.SiteScripts
import java.net.URLEncoder

class WitAnimeExtension : ProviderExtension {
    override val id = "witanime_extension"
    override val name = "witanime.you"
    override val baseUrl = "https://witanime.you"
    override val isAnime = true
    override val isMovie = false
    override val isSeries = false
    override val lang = "ar"
    override val iconUrl = ""

    override fun getSearchUrl(titleOriginal: String, titleClean: String): String {
        val encoded = URLEncoder.encode(titleOriginal, "UTF-8").replace("%20", "+")
        return "https://witanime.you/?search_param=animes&s=$encoded"
    }

    override fun getExtractionScript(isMovie: Boolean, episode: Int, title: String): String {
        return SiteScripts.getScriptForSite("witanime.you", isMovie, episode, title)
    }
}
