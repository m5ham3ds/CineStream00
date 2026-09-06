import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Add states for cancel dialog
state_old = """    var availableQualities by remember { mutableStateOf<List<com.example.utils.M3U8Parser.QualityInfo>>(emptyList()) }"""
state_new = """    var availableQualities by remember { mutableStateOf<List<com.example.utils.M3U8Parser.QualityInfo>>(emptyList()) }
    var showCancelConfirmDialog by remember { mutableStateOf(false) }"""
content = content.replace(state_old, state_new)

# Update Dialog properties
dialog_old = """    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {"""
dialog_new = """    Dialog(
        onDismissRequest = {
            if (isLoading || isExtractingQualities) {
                showCancelConfirmDialog = true
            } else {
                onDismiss()
            }
        },
        properties = DialogProperties(
            usePlatformDefaultWidth = false,
            dismissOnClickOutside = false,
            dismissOnBackPress = true
        )
    ) {"""
content = content.replace(dialog_old, dialog_new)

# Update Header UI
header_old = """                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
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
                        }
                        Spacer(modifier = Modifier.width(16.dp))
                        Column(
                            modifier = Modifier.weight(1f),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "اختر السيرفر",
                                color = Color.White,
                                style = MaterialTheme.typography.titleLarge,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )
                            Text(
                                text = "جاري الإتصال بالسيرفرات المتاحة...",
                                color = Color.Gray,
                                style = MaterialTheme.typography.bodySmall,
                                maxLines = 1,
                                overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                            )
                        }
                    }
                    IconButton(
                        onClick = onDismiss,
                        modifier = Modifier
                            .size(36.dp)
                            .background(Color(0xFF222225), CircleShape)
                            .border(1.dp, Color(0xFF333333), CircleShape)
                    ) {
                        Icon(Icons.Default.Close, contentDescription = "إغلاق", tint = Color.White, modifier = Modifier.size(18.dp))                    }
                }"""

header_new = """                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    if (availableQualities.isNotEmpty() || isExtractingQualities) {
                        IconButton(
                            onClick = { 
                                isExtractingQualities = false
                                availableQualities = emptyList()
                                selectedServerToExtract = null
                            },
                            modifier = Modifier
                                .size(48.dp)
                                .background(Color(0xFF222225), CircleShape)
                        ) {
                            Icon(
                                imageVector = androidx.compose.material.icons.Icons.Default.ArrowBack,
                                contentDescription = "Back",
                                tint = Color.White,
                                modifier = Modifier.size(24.dp)
                            )
                        }
                    } else {
                        Box(
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
                        }
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    Column(
                        modifier = Modifier.weight(1f),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        Text(
                            text = "اختر السيرفر",
                            color = Color.White,
                            style = MaterialTheme.typography.titleLarge,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                        Text(
                            text = "جاري الإتصال بالسيرفرات المتاحة...",
                            color = Color.Gray,
                            style = MaterialTheme.typography.bodySmall,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis
                        )
                    }
                    Spacer(modifier = Modifier.width(16.dp))
                    IconButton(
                        onClick = {
                            if (isLoading || isExtractingQualities) {
                                showCancelConfirmDialog = true
                            } else {
                                onDismiss()
                            }
                        },
                        modifier = Modifier
                            .size(36.dp)
                            .background(Color(0xFF222225), CircleShape)
                            .border(1.dp, Color(0xFF333333), CircleShape)
                    ) {
                        Icon(
                            imageVector = androidx.compose.material.icons.Icons.Default.Close,
                            contentDescription = "Close",
                            tint = Color.White,
                            modifier = Modifier.size(16.dp)
                        )
                    }
                }"""

content = content.replace(header_old, header_new)

# Add confirm dialog logic at the end of the box
dialog_end_old = """            }
        }
    }
}

@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color) {"""

dialog_end_new = """            }
        }
        
        if (showCancelConfirmDialog) {
            AlertDialog(
                onDismissRequest = { showCancelConfirmDialog = false },
                containerColor = Color(0xFF222225),
                titleContentColor = Color.White,
                textContentColor = Color.LightGray,
                title = {
                    Text(text = "إلغاء العملية", fontWeight = FontWeight.Bold)
                },
                text = {
                    Text(text = "العملية لا تزال جارية، هل أنت متأكد أنك تريد الإلغاء؟")
                },
                confirmButton = {
                    TextButton(
                        onClick = {
                            showCancelConfirmDialog = false
                            onDismiss()
                        }
                    ) {
                        Text("نعم، إلغاء", color = Color(0xFFFF1111))
                    }
                },
                dismissButton = {
                    TextButton(
                        onClick = { showCancelConfirmDialog = false }
                    ) {
                        Text("متابعة", color = Color.White)
                    }
                }
            )
        }
    }
}

@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color) {"""

content = content.replace(dialog_end_old, dialog_end_new)


# Fix the 'Extracting qualities' text logic
extract_old = """                } else if (isExtractingQualities) {
                    Spacer(modifier = Modifier.height(24.dp))
                    CircularProgressIndicator(color = activeColor, modifier = Modifier.size(48.dp))
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "جاري استخراج الجودات المتاحة...",
                        color = Color.White,
                        style = MaterialTheme.typography.titleMedium
                    )
                }"""

extract_new = """                } else if (isExtractingQualities) {
                    Spacer(modifier = Modifier.height(24.dp))
                    CircularProgressIndicator(color = activeColor, modifier = Modifier.size(48.dp))
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "جاري استخراج الجودات المتاحة...",
                        color = Color.White,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        textAlign = TextAlign.Center,
                        maxLines = 1,
                        overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                        modifier = Modifier.fillMaxWidth()
                    )
                }"""

content = content.replace(extract_old, extract_new)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

