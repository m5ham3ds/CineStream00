import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_block = """                if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie') && !loc.includes('play.php') && !loc.includes('video.php') && !loc.includes('/anime/') && !loc.includes('tvshow'))) {
                    var originalTitle = "${title.lowercase().replace("'", "").replace("\"", "")}";
                    var isSeries = originalTitle.includes(' - s') && originalTitle.includes('e');
                    var baseTitle = originalTitle;"""

new_block = """                // --- SMART SEARCH RESULT MATCHER ---
                if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie') && !loc.includes('play.php') && !loc.includes('video.php') && !loc.includes('/anime/') && !loc.includes('tvshow'))) {
                    // For finding elements by title, we need to pass the base title, not the lowercase version which might break the JS string escaping or variable replacement
                    var originalTitle = "${title.lowercase().replace("'", "").replace("\"", "")}";
                    var isSeries = originalTitle.includes(' - s') && originalTitle.includes('e');
                    var baseTitle = originalTitle;"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
        f.write(content)
    print("Replaced title JS block successfully!")
else:
    print("Could not find title JS block!")
