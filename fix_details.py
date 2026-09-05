import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

# Fix DownloadItem for Movie
pattern = r'(downloadRepository\.addToDownloads\(com\.example\.data\.model\.DownloadItem\(\s*id = movie\.id,\s*title = movie\.originalTitle \?: movie\.title,\s*posterUrl = movie\.posterUrl,\s*isMovie = true,)[\s\S]*?quality = serverName'
replacement = r'\1 quality = serverName'
content = re.sub(pattern, replacement, content)

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'w') as f:
    f.write(content)
