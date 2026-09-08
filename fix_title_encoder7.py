import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_block = """    val encodedPlusTitle = URLEncoder.encode(cleanTitle, "UTF-8").replace("%20", "+")
    val searchUrl = when (currentSiteName) {
        "witanime.you" -> "https://witanime.you/?search_param=animes&s=$encodedPlusTitle"
        "w1.anime4up.rest" -> "https://w1.anime4up.rest/?s=$encodedTitle"
        "animeblkom.net" -> "https://animeblkom.net/search?query=$encodedPlusTitle"
        "animeat.net" -> "https://animeat.net/"
        "arabanime.net" -> "https://www.arabanime.net/searchq"
        "det.animerco.org" -> "https://det.animerco.org/?s=$encodedPlusTitle"
        "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedPlusTitle"
        "tv10.egydead.live" -> "https://tv10.egydead.live/?s=$encodedPlusTitleOriginal"
        "a.qfilm.tv" -> "https://a.qfilm.tv/search.php?keywords=$encodedPlusTitleOriginal&video-id=#"
        "egybests.live" -> "http://egybests.live/?s=$encodedPlusTitleOriginal"
        "arabseed.wine" -> "https://www.arabseed.wine/?s=$encodedPlusTitleOriginal&type="
        "topcinema.io" -> "https://topcinema.io/"
        "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedPlusTitleOriginal&video-id="
        "arabseed-tv.com" -> "https://arabseed-tv.com/"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedPlusTitleOriginal&video-id=#"
        "stardima.com", "watch.stardima.com" -> "https://www.stardima.com/search?query=$encodedTitleOriginal"
        "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedPlusTitleOriginal&video-id="
        "laaroza.space" -> "https://laaroza.sbs/search.php?keywords=$encodedPlusTitleOriginal"
        else -> "https://$currentSiteName/?s=$encodedPlusTitleOriginal"
    }"""

new_block = """    val encodedPlusTitle = URLEncoder.encode(cleanTitle, "UTF-8").replace("%20", "+")
    
    // For general sites we use original Title so we don't break their search (they handle symbols themselves)
    // ONLY for specific sites that need cleaned titles (like tv10.egydead, etc) we use the cleaned version
    val searchUrl = when (currentSiteName) {
        "witanime.you" -> "https://witanime.you/?search_param=animes&s=$encodedPlusTitleOriginal"
        "w1.anime4up.rest" -> "https://w1.anime4up.rest/?s=$encodedTitleOriginal"
        "animeblkom.net" -> "https://animeblkom.net/search?query=$encodedPlusTitleOriginal"
        "animeat.net" -> "https://animeat.net/"
        "arabanime.net" -> "https://www.arabanime.net/searchq"
        "det.animerco.org" -> "https://det.animerco.org/?s=$encodedPlusTitleOriginal"
        "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedPlusTitleOriginal"
        
        // Sites that might need the cleaned title without symbols
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
        else -> "https://$currentSiteName/?s=$encodedPlusTitleOriginal"
    }"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Replaced title encoder successfully!")
else:
    print("Could not find title encoder block!")
