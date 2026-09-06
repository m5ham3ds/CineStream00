import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

content = content.replace(" || isExtractingQualities", "")
content = re.sub(r'\s*var isExtractingQualities by remember \{ mutableStateOf\(false\) \}', "", content)
content = re.sub(r'\s*var availableQualities by remember \{ mutableStateOf<List<com.example.utils.M3U8Parser.QualityInfo>>\(emptyList\(\)\) \}', "", content)
content = re.sub(r'\s*var selectedServerToExtract by remember \{ mutableStateOf<String\?>\(null\) \}', "", content)
content = re.sub(r'\s*var selectedServerUrlToExtract by remember \{ mutableStateOf<String\?>\(null\) \}', "", content)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

