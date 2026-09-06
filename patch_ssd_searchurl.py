import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

start_idx = content.find("val searchUrl = when {")
end_idx = content.find("}", start_idx) + 1

if start_idx != -1 and end_idx != -1:
    new_code = """val searchUrl = when (currentSiteName) {
        "tv10.egydead.live" -> "https://tv10.egydead.live/page/1/?s=$encodedTitle"
        "a.qfilm.tv" -> "https://a.qfilm.tv/search.php?keywords=$encodedTitle"
        "egybests.live" -> "https://egybests.live/?s=$encodedTitle&page=1"
        "arabseed.wine" -> "https://www.arabseed.wine/page/1/?s=$encodedTitle"
        "topcinema.io" -> "https://topcinema.io/search.php?keywords=$encodedTitle"
        "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedTitle"
        "arabseed-tv.com" -> "https://arabseed-tv.com/page/1/?s=$encodedTitle"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedTitle"
        "stardima.com" -> "https://www.stardima.com/search?query=$encodedTitle&page=1"
        "watch.stardima.com" -> "https://watch.stardima.com/watch/search_gcse-2/?s=$encodedTitle&page=1"
        "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedTitle"
        "laaroza.space" -> "https://laaroza.space/search.php?keywords=$encodedTitle"
        "witanime.you" -> "https://witanime.you/?search_param=animes&s=$encodedTitle"
        "w1.anime4up.rest" -> "https://w1.anime4up.rest/?search_param=animes&s=$encodedTitle"
        "animeblkom.net" -> "https://animeblkom.net/search?query=$encodedTitle"
        "animeat.net" -> "https://animeat.net/?search=$encodedTitle"
        "arabanime.net" -> "https://www.arabanime.net/?s=$encodedTitle"
        "det.animerco.org" -> "https://det.animerco.org/?s=$encodedTitle&page=1"
        "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedTitle&page=1"
        else -> "https://$currentSiteName/?s=$encodedTitle"
    }"""
    content = content[:start_idx] + new_code + content[end_idx:]

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
