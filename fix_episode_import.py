import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'fun selectEpisode(episode: com.example.data.model.Episode)',
    'fun selectEpisode(episode: com.example.domain.models.Episode)'
)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
