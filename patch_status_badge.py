import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_badge = """@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(16.dp))
            .background(Color(0xFF19191C))
            .border(1.dp, Color(0xFF2C2C2E), RoundedCornerShape(16.dp))
            .padding(horizontal = 10.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
        Spacer(modifier = Modifier.width(6.dp))
        Text(text, color = Color.LightGray, fontSize = 11.sp)
        Spacer(modifier = Modifier.width(6.dp))
        Box(modifier = Modifier.size(6.dp).background(statusColor, CircleShape))
    }
}"""

new_badge = """@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color) {
    Row(
        modifier = Modifier
            .clip(RoundedCornerShape(14.dp))
            .background(Color(0xFF19191C))
            .border(1.dp, Color(0xFF2C2C2E), RoundedCornerShape(14.dp))
            .padding(horizontal = 6.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(14.dp))
        Spacer(modifier = Modifier.width(4.dp))
        Text(text, color = Color.LightGray, fontSize = 10.sp, maxLines = 1)
        Spacer(modifier = Modifier.width(4.dp))
        Box(modifier = Modifier.size(6.dp).background(statusColor, CircleShape))
    }
}"""

content = content.replace(old_badge, new_badge)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)

