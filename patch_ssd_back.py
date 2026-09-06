import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_header = """                    Box(
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

new_header = """                    if (availableQualities.isNotEmpty() || isExtractingQualities) {
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
                                imageVector = androidx.compose.material.icons.Icons.AutoMirrored.Filled.ArrowBack,
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
                    }"""

content = content.replace(old_header, new_header)

# Make sure AutoMirrored.Filled.ArrowBack is imported
if "import androidx.compose.material.icons.automirrored.filled.ArrowBack" not in content:
    content = "import androidx.compose.material.icons.automirrored.filled.ArrowBack\n" + content

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

