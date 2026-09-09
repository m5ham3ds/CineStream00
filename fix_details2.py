import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# Fix MovieDetailsScreen signature
content = content.replace("fun MovieDetailsScreen(\n    onPersonClick: (String) -> Unit = {},\n    movieId: String, \n    onBack: () -> Unit,\n    onPlay: (String, String, String?, String?) -> Unit,\n    viewModel: MovieDetailsViewModel = viewModel(factory = ViewModelFactory())\n)",
"fun MovieDetailsScreen(\n    onPersonClick: (String) -> Unit = {},\n    movieId: String, \n    onBack: () -> Unit,\n    onPlay: (String, String, String?, String?) -> Unit,\n    onNavigateToExtensions: () -> Unit = {},\n    viewModel: MovieDetailsViewModel = viewModel(factory = ViewModelFactory())\n)")

# Fix SeriesDetailsScreen signature
content = content.replace("fun SeriesDetailsScreen(\n    onPersonClick: (String) -> Unit = {},\n    seriesId: String, \n    onBack: () -> Unit,\n    onPlay: (String, String, String?, String?) -> Unit,\n    viewModel: SeriesDetailsViewModel = viewModel(factory = ViewModelFactory())\n)",
"fun SeriesDetailsScreen(\n    onPersonClick: (String) -> Unit = {},\n    seriesId: String, \n    onBack: () -> Unit,\n    onPlay: (String, String, String?, String?) -> Unit,\n    onNavigateToExtensions: () -> Unit = {},\n    viewModel: SeriesDetailsViewModel = viewModel(factory = ViewModelFactory())\n)")

# Fix navController.navigate("extensions")
content = content.replace("navController.navigate(\"extensions\")", "onNavigateToExtensions()")

# Remove duplicate NoExtensionsDialog logic if I accidentally added it multiple times or to the wrong place
# Actually I replaced "showSourceSheet = true" with the if block, let's just make sure it's correct.

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
