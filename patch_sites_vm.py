import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_sites = """        val allAnimeSites = listOf("WitAnime", "Anime4up", "AnimeBlkom", "Animeat", "Arabanime", "Animerco", "AnimeLuxe", "Stardima", "Watch Stardima")
        val allMovieSeriesSites = listOf("EgyDead TV10", "QFilm", "TopCinema", "Laaroza", "Almeshkah", "ArabSeed Wine", "ArabSeed", "Egy Best", "CimaLight", "Brstej")

        val fallbackList = when {
            isAnime -> listOf("WitAnime", "Anime4up", "AnimeBlkom") + allAnimeSites.filter { it !in listOf("WitAnime", "Anime4up", "AnimeBlkom") }
            isMovie -> listOf("EgyDead TV10", "QFilm", "TopCinema") + allMovieSeriesSites.filter { it !in listOf("EgyDead TV10", "QFilm", "TopCinema") }
            else -> listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine") + allMovieSeriesSites.filter { it !in listOf("TopCinema", "EgyDead TV10", "Egy Best", "ArabSeed Wine") }
        }"""

new_sites = """        val allAnimeSites = listOf(
            "witanime.you", "w1.anime4up.rest", "animeblkom.net", "animeat.net", 
            "arabanime.net", "det.animerco.org", "vip.animeluxe.org"
        )
        val allMovieSeriesSites = listOf(
            "tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", 
            "topcinema.io", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", 
            "stardima.com", "watch.stardima.com", "uo.brstej.com", "laaroza.space"
        )

        val fallbackList = when {
            isAnime -> listOf("witanime.you", "w1.anime4up.rest", "animeblkom.net") + allAnimeSites.filter { it !in listOf("witanime.you", "w1.anime4up.rest", "animeblkom.net") }
            isMovie -> listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live") + allMovieSeriesSites.filter { it !in listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live") }
            else -> listOf("topcinema.io", "stardima.com", "tv10.egydead.live") + allMovieSeriesSites.filter { it !in listOf("topcinema.io", "stardima.com", "tv10.egydead.live") }
        }"""

content = content.replace(old_sites, new_sites)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
