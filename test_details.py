import re

with open('app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt', 'r') as f:
    content = f.read()

print("FOUND onPlay in DetailsScreens:")
matches = re.finditer(r'onPlay = { url, serverName, website ->(.*?)}', content, re.DOTALL)
for m in matches:
    print(m.group(1))

