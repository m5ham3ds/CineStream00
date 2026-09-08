with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_search_urls = """        "arabseed.wine" -> "https://www.arabseed.wine/?s=$encodedPlusTitle&type="
        "topcinema.io" -> "https://topcinema.io/"
        "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedPlusTitle&video-id="
        "arabseed-tv.com" -> "https://arabseed-tv.com/"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedPlusTitle&video-id=#" """

new_search_urls = """        "arabseed.wine" -> "https://www.arabseed.wine/?s=$encodedPlusTitle&type="
        "topcinema.io" -> "https://topcinema.io/?s=$encodedPlusTitle"
        "z1.almeshkah.net" -> "https://z1.almeshkah.net/search.php?keywords=$encodedPlusTitle&video-id="
        "arabseed-tv.com" -> "https://arabseed-tv.com/?s=$encodedPlusTitle"
        "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedPlusTitle&video-id=#" """

content = content.replace(old_search_urls, new_search_urls)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
