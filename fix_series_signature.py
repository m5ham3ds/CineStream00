import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace("fun SeriesDetailsScreen(\n    onPersonClick: (String) -> Unit = {},\n    seriesId: String,\n    onBack: () -> Unit,\n    onPlay: (String, String, String?, String?) -> Unit\n) {", 
"fun SeriesDetailsScreen(\n    onPersonClick: (String) -> Unit = {},\n    seriesId: String,\n    onBack: () -> Unit,\n    onPlay: (String, String, String?, String?) -> Unit,\n    onNavigateToExtensions: () -> Unit = {}\n) {")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
