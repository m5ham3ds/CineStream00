import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Add ExtensionManager import
if "import com.example.extensions.ExtensionManager" not in content:
    content = content.replace("import androidx.compose.ui.unit.sp", "import androidx.compose.ui.unit.sp\nimport com.example.extensions.ExtensionManager")

# Replace priority lists
replacement = """
    val installedExtensions = ExtensionManager.installedExtensions.collectAsState().value
    val prioritySites = installedExtensions.filter { 
        if (isAnime) it.isAnime else if (isMovie) it.isMovie else it.isSeries 
    }
    
    // Fallback if none matched but dialog was opened
    val safeSites = if (prioritySites.isNotEmpty()) prioritySites else installedExtensions
"""

content = re.sub(r'val priorityAnimeSites = listOf\([^)]+\)\s*val priorityMovieSites = listOf\([^)]+\)\s*val prioritySeriesSites = listOf\([^)]+\)\s*val prioritySites = if \(isAnime\) priorityAnimeSites else if \(isMovie\) priorityMovieSites else prioritySeriesSites', replacement, content)

# Update states that rely on prioritySites being List<String> instead of List<ProviderExtension>
content = content.replace("var currentSiteName by remember { mutableStateOf(prioritySites[0]) }", "var currentExtension by remember { mutableStateOf(safeSites[0]) }\n    var currentSiteName = currentExtension.name")

# Oh wait, we need to find all references to `prioritySites` and `currentSiteName`
# `prioritySites.size` still works.
# `prioritySites.size.coerceAtLeast(1)` works.
# `currentSiteName` is now a computed property, but wait, `currentSiteName` might be reassigned.
# Let's see if it's reassigned.
