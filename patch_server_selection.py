import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Add states for quality extraction
new_states = """
    var extractedServers by remember { mutableStateOf<List<String>>(emptyList()) }
    var extractedServerLinks by remember { mutableStateOf<Map<String, String>>(emptyMap()) }
    var finalWatchUrl by remember { mutableStateOf<String?>(null) }
    var isFailed by remember { mutableStateOf(false) }
    var bypassStatus by remember { mutableStateOf("CHECKING_CLOUDFLARE") }
    var showCancelConfirmDialog by remember { mutableStateOf(false) }

    // --- Quality Extraction States ---
    var selectedServerForQuality by remember { mutableStateOf<String?>(null) }
    var isExtractingQuality by remember { mutableStateOf(false) }
    var qualityExtractionMessage by remember { mutableStateOf("جاري استخراج الجودات المتاحة...") }
    var extractedQualities by remember { mutableStateOf<List<com.example.utils.M3U8Parser.QualityInfo>>(emptyList()) }
"""
content = re.sub(
    r'var extractedServers by remember.*showCancelConfirmDialog by remember \{ mutableStateOf\(false\) \}',
    new_states.strip(),
    content,
    flags=re.DOTALL
)

# Add HiddenVideoExtractor for Quality when selectedServerForQuality != null
hidden_video_extractor_logic = """
            }
        }
        
        // Hidden Extractor for Quality
        if (isExtractingQuality && selectedServerForQuality != null) {
            val serverUrl = extractedServerLinks[selectedServerForQuality] ?: finalWatchUrl ?: searchUrl
            HiddenVideoExtractor(
                url = serverUrl,
                isMovie = isMovie,
                season = season,
                episode = episode,
                targetServer = selectedServerForQuality,
                targetServerId = null, // Or try to get it if available
                onVideoUrlFound = { url ->
                    if (url.contains(".m3u8")) {
                        coroutineScope.launch {
                            qualityExtractionMessage = "جاري تحليل الجودات..."
                            val qualities = com.example.utils.M3U8Parser.getQualities(url)
                            extractedQualities = qualities
                            isExtractingQuality = false
                        }
                    } else {
                        // Not an m3u8, just show default
                        extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("جودة أصلية (Default)", url))
                        isExtractingQuality = false
                    }
                },
                onIframeUrlFound = { iframeUrl ->
                    // Sometimes we get a new iframe url, we should probably follow it or just return it as quality
                    extractedQualities = listOf(com.example.utils.M3U8Parser.QualityInfo("جودة أصلية (Default)", iframeUrl))
                    isExtractingQuality = false
                }
            )
        }
        
        if (showCancelConfirmDialog) {
"""
content = re.sub(
    r'\}[\s]*\}[\s]*if \(showCancelConfirmDialog\)',
    hidden_video_extractor_logic.strip(),
    content
)

# Update the rendering of extractedServers vs extractingQuality vs Qualities List
rendering_logic = """
                } else if (extractedServers.isNotEmpty()) {
                    if (selectedServerForQuality != null) {
                        if (isExtractingQuality) {
                            CircularProgressIndicator(
                                color = Color(0xFFE50914),
                                modifier = Modifier.size(50.dp)
                            )
                            Spacer(modifier = Modifier.height(16.dp))
                            Text(
                                text = qualityExtractionMessage,
                                color = Color.White,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "السيرفر: $selectedServerForQuality",
                                color = Color.Gray,
                                style = MaterialTheme.typography.bodySmall
                            )
                        } else if (extractedQualities.isNotEmpty()) {
                            Text(
                                text = "اختر الجودة ($selectedServerForQuality)",
                                color = Color(0xFFE50914),
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            
                            LazyColumn(
                                modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp),
                                verticalArrangement = Arrangement.spacedBy(8.dp)
                            ) {
                                items(extractedQualities) { quality ->
                                    Card(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .clickable {
                                                val serverAndQuality = "$selectedServerForQuality - ${quality.name}"
                                                onPlay(quality.url, serverAndQuality, currentSiteName)
                                            },
                                        colors = CardDefaults.cardColors(
                                            containerColor = Color(0xFF222225)
                                        ),
                                        shape = RoundedCornerShape(12.dp)
                                    ) {
                                        Row(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .padding(16.dp),
                                            verticalAlignment = Alignment.CenterVertically,
                                            horizontalArrangement = Arrangement.Center
                                        ) {
                                            Text(
                                                text = quality.name,
                                                color = Color.White,
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold
                                            )
                                        }
                                    }
                                }
                            }
                            
                            Spacer(modifier = Modifier.height(16.dp))
                            TextButton(onClick = { 
                                selectedServerForQuality = null
                                extractedQualities = emptyList()
                            }) {
                                Text("العودة لاختيار سيرفر آخر", color = Color.LightGray)
                            }
                        }
                    } else {
                        Text(
                            text = "تم جلب السيرفرات من: $currentSiteName",
                            color = Color(0xFF00C853),
                            style = MaterialTheme.typography.labelLarge,
                            modifier = Modifier.padding(bottom = 16.dp)
                        )
                        
                        LazyColumn(
                            modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp),
                            verticalArrangement = Arrangement.spacedBy(8.dp)
                        ) {
                            items(extractedServers) { server ->
                                Card(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .clickable {
                                            selectedServerForQuality = server
                                            isExtractingQuality = true
                                            extractedQualities = emptyList()
                                        },
                                    colors = CardDefaults.cardColors(
                                        containerColor = Color(0xFF222225)
                                    ),
                                    shape = RoundedCornerShape(12.dp)
                                ) {
                                    Row(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(16.dp),
                                        verticalAlignment = Alignment.CenterVertically,
                                        horizontalArrangement = Arrangement.Center
                                    ) {
                                        Text(
                                            text = server,
                                            color = Color.White,
                                            style = MaterialTheme.typography.titleMedium,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
"""

content = re.sub(
    r'\} else if \(extractedServers\.isNotEmpty\(\)\) \{.*\}\s*\}\s*\}\s*\}',
    rendering_logic.strip(),
    content,
    flags=re.DOTALL
)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

print("Patching complete.")
