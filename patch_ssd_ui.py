import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_ui = """                } else if (extractedServers.isNotEmpty()) {
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
                                        onPlay(extractedServerLinks[server] ?: finalWatchUrl ?: searchUrl, server, currentSiteName)
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
                }"""

new_ui = """                } else if (isExtractingQualities) {
                    Spacer(modifier = Modifier.height(24.dp))
                    CircularProgressIndicator(color = activeColor, modifier = Modifier.size(48.dp))
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "جاري استخراج الجودات المتاحة...",
                        color = Color.White,
                        style = MaterialTheme.typography.titleMedium
                    )
                } else if (availableQualities.isNotEmpty()) {
                    Text(
                        text = "اختر الجودة المناسبة:",
                        color = Color(0xFF00C853),
                        style = MaterialTheme.typography.labelLarge,
                        modifier = Modifier.padding(bottom = 16.dp)
                    )
                    
                    LazyColumn(
                        modifier = Modifier.fillMaxWidth().heightIn(max = 300.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        items(availableQualities) { quality ->
                            Card(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .clickable {
                                        onPlay(quality.url, "${selectedServerToExtract} - ${quality.name}", currentSiteName)
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
                                    Icon(
                                        imageVector = androidx.compose.material.icons.Icons.Outlined.Storage,
                                        contentDescription = null,
                                        tint = Color.White,
                                        modifier = Modifier.size(20.dp)
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
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
                } else if (extractedServers.isNotEmpty()) {
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
                                        selectedServerToExtract = server
                                        selectedServerUrlToExtract = extractedServerLinks[server] ?: finalWatchUrl ?: searchUrl
                                        availableQualities = emptyList()
                                        isExtractingQualities = true
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
                }"""

content = content.replace(old_ui, new_ui)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

