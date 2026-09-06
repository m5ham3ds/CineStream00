import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# I want to replace everything from "if (selectedTrailerId != null) {" inside SeriesDetailsScreen
# up to "// Seasons & Episodes"

start_str = "                if (selectedTrailerId != null) {"
end_str = "                // Seasons & Episodes"

# Find SeriesDetailsScreen
func_start = content.find("fun SeriesDetailsScreen(")
if func_start != -1:
    idx1 = content.find(start_str, func_start)
    idx2 = content.find(end_str, idx1)
    
    if idx1 != -1 and idx2 != -1:
        new_top = """                val firstUnplayedEpisode = uiState.episodes.firstOrNull { !watchedEpisodeIds.contains(it.id) } ?: uiState.episodes.firstOrNull()

                // Hero Image or Video Player
                if (selectedTrailerId != null) {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(16f/9f)) {
                        com.example.ui.components.InlineYouTubePlayer(
                            videoId = selectedTrailerId!!,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                        Text(text = series.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("${series.year} • ${series.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(18.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(String.format("%.1f", series.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                            }
                            Badge(containerColor = Color.DarkGray) { Text("18+", color = MaterialTheme.colorScheme.onBackground) }
                        }
                    }
                } else {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {
                        AsyncImage(
                            model = series.posterUrl.takeIf { it.isNotBlank() } ?: series.backdropUrl,
                            contentDescription = series.title,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                        Box(modifier = Modifier.fillMaxSize().background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, Color.Black.copy(alpha=0.6f), MaterialTheme.colorScheme.background),
                                startY = 0f
                            )
                        ))
                        Column(
                            modifier = Modifier.align(Alignment.BottomStart).padding(16.dp)
                        ) {
                            Text(text = series.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("${series.year} • ${series.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Star, contentDescription = "Rating", tint = Color(0xFFFFC107), modifier = Modifier.size(18.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text(String.format("%.1f", series.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                }
                                Badge(containerColor = Color.DarkGray) { Text("18+", color = MaterialTheme.colorScheme.onBackground) } // Placeholder for age rating
                            }
                        }
                    }
                }
                
                // Action Buttons
                Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Button(
                        onClick = {
                            if (firstUnplayedEpisode != null) {
                                selectedEpisodeForSource = firstUnplayedEpisode
                                isDownloadMode = false
                            } else {
                                Toast.makeText(context, "No episodes available", Toast.LENGTH_SHORT).show()
                            }
                        },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = "Play", tint = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(stringResource(R.string.play), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                    }
                    IconButton(
                        onClick = {
                            showBatchDownloadSheet = true
                        },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        Icon(Icons.Default.Download, contentDescription = "Download", tint = MaterialTheme.colorScheme.onBackground)
                    }
                    IconButton(
                        onClick = {
                            scope.launch {
                                val item = LibraryItem(id = series.id, title = series.originalTitle ?: series.title, posterUrl = series.posterUrl, isMovie = false)
                                if (isFavorite) libraryRepository.removeFromLibrary(item)
                                else libraryRepository.addToLibrary(item)
                            }
                        },
                        modifier = Modifier.size(50.dp).background(Color.DarkGray, CircleShape)
                    ) {
                        Icon(if (isFavorite) Icons.Default.Bookmark else Icons.Default.BookmarkBorder, contentDescription = "Favorite", tint = MaterialTheme.colorScheme.onBackground)
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Trailers
                if (series.trailers.isNotEmpty()) {
                    Text(stringResource(R.string.trailers), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(series.trailers) { trailer ->
                            TrailerCard(trailer) {
                                selectedTrailerId = trailer.key
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(24.dp))
                }
                
                // Overview
                Text(stringResource(R.string.overview), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                Spacer(modifier = Modifier.height(8.dp))
                Text(series.overview, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(horizontal = 16.dp))
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Cast
                if (series.cast.isNotEmpty()) {
                    Text(stringResource(R.string.cast), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        items(series.cast) { CastMemberCard(it) { onPersonClick(it.id) } }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
"""
        content = content[:idx1] + new_top + content[idx2:]
        with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
            f.write(content)
        print("Success: Patched SeriesDetailsScreen")
    else:
        print("Error: Could not find start or end block")
