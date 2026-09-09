import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Replace the priorityLists if they still exist
content = re.sub(
    r'val priorityAnimeSites = listOf.*?val prioritySites = if \(isAnime\).*?\n',
    """
    val installedExtensions = ExtensionManager.installedExtensions.collectAsState().value
    val prioritySites = installedExtensions.filter { 
        if (isAnime) it.isAnime else if (isMovie) it.isMovie else it.isSeries 
    }
    val safeSites = if (prioritySites.isNotEmpty()) prioritySites else installedExtensions
    """,
    content,
    flags=re.DOTALL
)

# Replace currentSiteName state definition
content = re.sub(
    r'var currentSiteName by remember \{ mutableStateOf\(.*?\) \}',
    """var currentExtension by remember { mutableStateOf(safeSites[0]) }
    val currentSiteName = currentExtension.name""",
    content
)

# Replace assignment to currentSiteName
content = content.replace("currentSiteName = prioritySites[currentSiteIndex]", "currentExtension = safeSites[currentSiteIndex]")
content = content.replace("currentSiteName = prioritySites[0]", "currentExtension = safeSites[0]")

# Replace searchUrl block entirely
# `val searchUrl = when (currentSiteName) { ... }` -> `val searchUrl = currentExtension.getSearchUrl(baseTitle, cleanTitle)`
# First find the block
search_block = re.search(r'val searchUrl = when \(currentSiteName\) \{.*?\n    \}', content, re.DOTALL)
if search_block:
    content = content.replace(search_block.group(0), "val searchUrl = currentExtension.getSearchUrl(baseTitle, cleanTitle)")

# Replace getScriptForSite
content = content.replace("com.example.ui.screens.player.SiteScripts.getScriptForSite(currentSiteName, isMovie, episode, title)", "currentExtension.getExtractionScript(isMovie, episode, title)")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
