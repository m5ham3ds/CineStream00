import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_block = """    val cleanTitle = baseTitle.replace(Regex("[^a-zA-Z0-9\\\\s]"), " ").replace(Regex("\\\\s+"), " ").trim()
    val encodedTitle = URLEncoder.encode(cleanTitle, "UTF-8")
    val encodedPlusTitle = URLEncoder.encode(cleanTitle, "UTF-8").replace("%20", "+")"""

new_block = """    val cleanTitle = baseTitle.replace(Regex("[^a-zA-Z0-9\\\\s]"), " ").replace(Regex("\\\\s+"), " ").trim()
    // For sites like tv10.egydead.live we actually need the original encoded title, not the cleaned one!
    // Example: tv10.egydead.live/?s=Spider-Man%3A+Brand+New+Day
    val encodedTitleOriginal = URLEncoder.encode(baseTitle, "UTF-8")
    val encodedPlusTitleOriginal = URLEncoder.encode(baseTitle, "UTF-8").replace("%20", "+")
    val encodedTitle = URLEncoder.encode(cleanTitle, "UTF-8")
    val encodedPlusTitle = URLEncoder.encode(cleanTitle, "UTF-8").replace("%20", "+")"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
        f.write(content)
    print("Replaced title encoder successfully!")
else:
    print("Could not find title encoder block!")
