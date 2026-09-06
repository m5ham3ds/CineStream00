import re

with open('app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt', 'r') as f:
    content = f.read()

old_title = """        Text(
            text = "Series",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onBackground,
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
        )
"""

if old_title in content:
    content = content.replace(old_title, "")
    with open('app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt', 'w') as f:
        f.write(content)
    print("Fixed SeriesScreen title.")
else:
    print("Could not find SeriesScreen title.")
