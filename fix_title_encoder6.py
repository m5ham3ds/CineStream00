import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_block = """        "tv10.egydead.live" -> "https://tv10.egydead.live/?s=$encodedPlusTitle"
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
    }"""

new_block = """        "tv10.egydead.live" -> "https://tv10.egydead.live/?s=$encodedPlusTitleOriginal"
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

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Replaced title encoder successfully!")
else:
    print("Could not find title encoder block!")
