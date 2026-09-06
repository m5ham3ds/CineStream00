import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Add retryTrigger
if 'var retryTrigger' not in content:
    content = re.sub(
        r'var showCancelConfirmDialog by remember \{ mutableStateOf\(false\) \}',
        'var showCancelConfirmDialog by remember { mutableStateOf(false) }\n    var retryTrigger by remember { mutableIntStateOf(0) }',
        content
    )

# Fix "جاري استخراج الجودات" text to be one line
text_quality = """                            Text(
                                text = qualityExtractionMessage,
                                color = Color.White,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold
                            )"""
text_quality_new = """                            Text(
                                text = qualityExtractionMessage,
                                color = Color.White,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.Bold,
                                textAlign = TextAlign.Center,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )"""
content = content.replace(text_quality, text_quality_new)

# Fix back button in header
header_box = """                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(Color(0xFF330000), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = androidx.compose.material.icons.Icons.Outlined.CloudDownload,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(24.dp)
                        )
                    }"""
header_box_new = """                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .background(Color(0xFF330000), CircleShape)
                            .clickable {
                                if (selectedServerForQuality != null) {
                                    selectedServerForQuality = null
                                    extractedQualities = emptyList()
                                    isExtractingQuality = false
                                }
                            },
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = if (selectedServerForQuality != null) androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack else androidx.compose.material.icons.Icons.Outlined.CloudDownload,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(24.dp)
                        )
                    }"""
content = content.replace(header_box, header_box_new)

# Add "البحث في موقع آخر" in the extracted servers list
search_another = """                                }
                            }
                        }
                    }
                }"""
search_another_new = """                                }
                            }
                        }
                        
                        if (currentSiteIndex < prioritySites.size - 1) {
                            Spacer(modifier = Modifier.height(16.dp))
                            TextButton(
                                onClick = {
                                    currentSiteIndex++
                                    currentSiteName = prioritySites[currentSiteIndex]
                                    extractedServers = emptyList()
                                    extractedServerLinks = emptyMap()
                                    isLoading = true
                                    isFailed = false
                                    retryTrigger++
                                },
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                Text("البحث في موقع آخر", color = Color(0xFF00C853))
                            }
                        }
                    }
                }"""
content = content.replace(search_another, search_another_new)

# Replace "isFailed" with retry button
is_failed_block = """                } else if (isFailed) {
                    Text(
                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                        color = Color(0xFFFF1111),
                        style = MaterialTheme.typography.bodyLarge,
                        textAlign = TextAlign.Center
                    )
                } else if (extractedServers.isNotEmpty()) {"""
is_failed_new = """                } else if (isFailed) {
                    Text(
                        text = "عذراً، لم نتمكن من العثور على سيرفرات تعمل لهذا العمل في جميع المواقع المدعومة.",
                        color = Color(0xFFFF1111),
                        style = MaterialTheme.typography.bodyLarge,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(24.dp))
                    Button(
                        onClick = {
                            isFailed = false
                            isLoading = true
                            currentSiteIndex = 0
                            currentSiteName = prioritySites[0]
                            retryTrigger++
                        },
                        modifier = Modifier.fillMaxWidth().height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE50914))
                    ) {
                        Text("إعادة المحاولة مجدداً", color = Color.White, fontWeight = FontWeight.Bold)
                    }
                } else if (extractedServers.isNotEmpty()) {"""
content = content.replace(is_failed_block, is_failed_new)

# Add key to HiddenVideoExtractor
extractor_old = """        if (isLoading && !isFailed) {
            HiddenVideoExtractor("""
extractor_new = """        if (isLoading && !isFailed) {
            key(retryTrigger) {
                HiddenVideoExtractor("""
extractor_old_end = """                onServersFound = { servers ->"""
extractor_new_end = """                onServersFound = { servers ->"""
# wait, replacing key is slightly tricky with python if we don't match the closing bracket.
# Let's do it with regex.

content = re.sub(
    r'if \(isLoading && !isFailed\) \{\s*HiddenVideoExtractor\(.*?(?=\s*\}\s*// Hidden Extractor for Quality)',
    lambda m: m.group(0).replace('HiddenVideoExtractor(', 'key(retryTrigger) {\n                HiddenVideoExtractor(') + '\n            }',
    content,
    flags=re.DOTALL
)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("done")
