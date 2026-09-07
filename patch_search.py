import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Update URL encodings
if "val encodedPlusTitle =" not in content:
    content = content.replace('val encodedTitle = URLEncoder.encode(title, "UTF-8")', 
'''val encodedTitle = URLEncoder.encode(title, "UTF-8")
    val encodedPlusTitle = URLEncoder.encode(title, "UTF-8").replace("%20", "+")''')

# Update searchUrl block
old_search_url_block = re.search(r'val searchUrl = when \(currentSiteName\) \{.*?(?=if \(isLoading && !isFailed\))', content, re.DOTALL)
if old_search_url_block:
    new_search_url_block = """val searchUrl = when (currentSiteName) {
        "witanime.you" -> "https://witanime.you/?search_param=animes&s=$encodedPlusTitle"
        "w1.anime4up.rest" -> "https://w1.anime4up.rest/?s=$encodedTitle"
        "animeblkom.net" -> "https://animeblkom.net/search?query=$encodedPlusTitle"
        "animeat.net" -> "https://animeat.net/"
        "arabanime.net" -> "https://www.arabanime.net/searchq"
        "det.animerco.org" -> "https://det.animerco.org/?s=$encodedPlusTitle"
        "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedPlusTitle"
        "tv10.egydead.live" -> "https://tv10.egydead.live/?s=$encodedPlusTitle"
        "a.qfilm.tv" -> "https://a.qfilm.tv/search.php?keywords=$encodedPlusTitle&video-id=#"
        "egybests.live" -> "http://egybests.live/?s=$encodedPlusTitle"
        "arabseed.wine" -> "https://www.arabseed.wine/?s=$encodedPlusTitle&type="
        "topcinema.io" -> "https://topcinema.io/"
        "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedPlusTitle&video-id="
        "arabseed-tv.com" -> "https://arabseed-tv.com/"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedPlusTitle&video-id=#"
        "stardima.com", "watch.stardima.com" -> "https://www.stardima.com/search?query=$encodedTitle"
        "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedPlusTitle&video-id="
        "laaroza.space" -> "https://laaroza.sbs/search.php?keywords=$encodedPlusTitle"
        else -> "https://$currentSiteName/?s=$encodedPlusTitle"
    }

    """
    content = content.replace(old_search_url_block.group(0), new_search_url_block)

# Update getScriptForSite call
content = content.replace("SiteScripts.getScriptForSite(currentSiteName, isMovie, episode)", "SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)")

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("ServerSelectionDialog.kt patched")
