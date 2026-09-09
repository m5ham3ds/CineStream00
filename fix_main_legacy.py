import os

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

legacy_import = "import com.example.extensions.providers.LegacySiteExtension\n"
if legacy_import not in content:
    content = content.replace("import com.example.extensions.providers.WitAnimeExtension\n", "import com.example.extensions.providers.WitAnimeExtension\n" + legacy_import)

register_code = """
    val legacyAnime = listOf("w1.anime4up.rest", "animeblkom.net", "animeat.net", "arabanime.net", "det.animerco.org", "vip.animeluxe.org")
    val legacyMovies = listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", "topcinema.io", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", "stardima.com", "watch.stardima.com", "uo.brstej.com", "laaroza.space")
    
    legacyAnime.forEach { name ->
        ExtensionManager.registerExtension(LegacySiteExtension(name, name, "https://$name", true, false, false))
    }
    legacyMovies.forEach { name ->
        ExtensionManager.registerExtension(LegacySiteExtension(name, name, "https://$name", false, true, true))
    }
"""

content = content.replace("ExtensionManager.registerExtension(WitAnimeExtension())", "ExtensionManager.registerExtension(WitAnimeExtension())\n" + register_code)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
