import re

with open('app/src/main/java/com/example/ui/components/DownloadQualitySheet.kt', 'r') as f:
    content = f.read()

content = content.replace("fun DownloadQualitySheet(", "fun DownloadQualitySheet(\n    qualities: List<String> = listOf(\"1080p\", \"720p\", \"480p\"),")
content = content.replace("""    val qualities = listOf(
        "1080p (FHD)", 
        "720p (HD)", 
        "480p (SD)"
    )""", "")

with open('app/src/main/java/com/example/ui/components/DownloadQualitySheet.kt', 'w') as f:
    f.write(content)
