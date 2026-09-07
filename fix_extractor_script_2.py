import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

# Add website parameter
content = content.replace(
    '    targetServerId: String? = null,',
    '    targetServerId: String? = null,\n    website: String = "",'
)

# Use website instead of UrlHelper
content = content.replace(
    'com.example.utils.UrlHelper.getDomainName(url)',
    'website'
)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
