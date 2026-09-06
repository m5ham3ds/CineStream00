import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_code = re.search(r"val priorityAnimeSites = listOf\([^)]+\)\s*val priorityMovieSites = listOf\([^)]+\)\s*val prioritySeriesSites = listOf\([^)]+\)", content).group(0)

new_code = """val priorityAnimeSites = listOf("witanime.you", "w1.anime4up.rest", "animeblkom.net", "animeat.net", "arabanime.net", "det.animerco.org", "vip.animeluxe.org")
    val priorityMovieSites = listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", "topcinema.io", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", "stardima.com", "watch.stardima.com", "uo.brstej.com", "laaroza.space")
    val prioritySeriesSites = listOf("topcinema.io", "stardima.com", "tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", "watch.stardima.com", "uo.brstej.com", "laaroza.space")"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
