with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_cond = "if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie'))) {"
new_cond = "if (serverItems.length === 0 && (!loc.includes('watch') && !loc.includes('episode') && !loc.includes('movie') && !loc.includes('play.php') && !loc.includes('video.php'))) {"

content = content.replace(old_cond, new_cond)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
