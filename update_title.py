import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

# Add title to signature
content = content.replace("website: String = \"\",", "website: String = \"\",\n    title: String = \"\",")

# Pass title to getScriptForSite
content = content.replace(
    'val siteScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(\n                                website, \n                                isMovie, \n                                episode, \n                                ""\n                            )',
    'val siteScript = com.example.ui.screens.player.SiteScripts.getScriptForSite(\n                                website, \n                                isMovie, \n                                episode, \n                                title\n                            )'
)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    ps_content = f.read()

# Add title = uiState.title to HiddenVideoExtractor call
ps_content = ps_content.replace(
    'HiddenVideoExtractor(\n                    url = url,\n                    isMovie = uiState.isMovie,\n                    season = uiState.currentSeasonNumber,\n                    episode = uiState.currentEpisodeNumber,\n                    targetServer = uiState.serverToChange,\n                    targetServerId = uiState.serverIdToChange,\n                    website = uiState.currentWebsite,',
    'HiddenVideoExtractor(\n                    url = url,\n                    isMovie = uiState.isMovie,\n                    season = uiState.currentSeasonNumber,\n                    episode = uiState.currentEpisodeNumber,\n                    targetServer = uiState.serverToChange,\n                    targetServerId = uiState.serverIdToChange,\n                    website = uiState.currentWebsite,\n                    title = uiState.title,'
)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(ps_content)

