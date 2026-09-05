import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# Add extractedServerLinks state
state_code = "var extractedServers by remember { mutableStateOf<List<String>>(emptyList()) }"
new_state_code = "var extractedServers by remember { mutableStateOf<List<String>>(emptyList()) }\n    var extractedServerLinks by remember { mutableStateOf<Map<String, String>>(emptyMap()) }"
content = content.replace(state_code, new_state_code)

# Modify onPlay to use the direct link
play_code = "onPlay(finalWatchUrl ?: searchUrl, server, currentSiteName)"
new_play_code = "onPlay(extractedServerLinks[server] ?: finalWatchUrl ?: searchUrl, server, currentSiteName)"
content = content.replace(play_code, new_play_code)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

