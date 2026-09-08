with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_search = """    val encodedTitle = URLEncoder.encode(title, "UTF-8")
    val encodedPlusTitle = URLEncoder.encode(title, "UTF-8").replace("%20", "+")"""

new_search = """    val baseTitle = if (title.contains(" - S") && title.contains("E")) {
        title.substringBefore(" - S").trim()
    } else {
        title
    }
    val encodedTitle = URLEncoder.encode(baseTitle, "UTF-8")
    val encodedPlusTitle = URLEncoder.encode(baseTitle, "UTF-8").replace("%20", "+")"""

content = content.replace(old_search, new_search)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
