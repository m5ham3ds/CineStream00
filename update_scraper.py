import re

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'r') as f:
    content = f.read()

# We want to add a fallback to return the search URL instead of null.
# Let's extract the search URLs and create a helper function at the end of the file.

fallback_logic = """
    private fun getSearchUrl(website: String, query: String): String {
        val encodedQuery = java.net.URLEncoder.encode(query, "UTF-8")
        return when (website) {
            "animeat.net" -> "https://animeat.net/?s=$encodedQuery"
            "arabseed-tv.com" -> "https://arabseed-tv.com/page/1/?s=$encodedQuery"
            "arabseed.wine" -> "https://www.arabseed.wine/page/1/?s=$encodedQuery"
            "det.animerco.org" -> "https://det.animerco.org/?s=$encodedQuery&page=1"
            "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedQuery"
            "egybests.live" -> "https://egybests.live/?s=$encodedQuery&page=1"
            "stardima.com" -> "https://www.stardima.com/search?query=$encodedQuery&page=1"
            "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedQuery"
            "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedQuery&page=1"
            "watch.stardima.com" -> "https://watch.stardima.com/watch/search_gcse-2/?s=$encodedQuery&page=1"
            "witanime.you", "w1.anime4up.rest", "animeblkom.net" -> "https://$website/?search_param=animes&s=$encodedQuery"
            "topcinema.io", "laaroza.space", "z1.almeshkah.net" -> "https://$website/search.php?keywords=$encodedQuery"
            else -> "https://$website/?s=$encodedQuery"
        }
    }
}
"""

content = content.replace("}\n}", "}\n" + fallback_logic)

# Replace returns of null with the fallback
# We replace `return@withContext null` with `return@withContext getSearchUrl(website, query)`
# BUT we only want to do this inside the `getWatchUrl` function, not generally.

# Since all `return@withContext null` inside `getWatchUrl` should really fallback to the search URL:
content = re.sub(r'return@withContext null', r'return@withContext getSearchUrl(website, query)', content)

with open('app/src/main/java/com/example/data/repository/ScraperRepository.kt', 'w') as f:
    f.write(content)

