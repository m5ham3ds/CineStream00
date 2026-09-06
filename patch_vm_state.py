import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'r') as f:
    content = f.read()

old_state = """    // Server
    val availableServers: List<String> = emptyList(),
    val currentServer: String = "","""

new_state = """    // Server
    val availableServers: List<String> = emptyList(),
    val currentServer: String = "",
    val availableServerLinks: Map<String, String> = emptyMap(),
    val availableServerIds: Map<String, String> = emptyMap(),
    val serverIdToChange: String? = null,"""

content = content.replace(old_state, new_state)

with open('app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt', 'w') as f:
    f.write(content)
