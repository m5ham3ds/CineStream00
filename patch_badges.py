import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

old_badges = """                    // Badges Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(4.dp, Alignment.CenterHorizontally),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        StatusBadge(
                            text = if (isCloudflare) "جاري التحقق" else "تم التحقق",
                            icon = androidx.compose.material.icons.Icons.Outlined.CheckCircle,
                            statusColor = activeColor
                        )
                        StatusBadge(
                            text = "تحديث البيانات",
                            icon = androidx.compose.material.icons.Icons.Outlined.Sync,
                            statusColor = activeColor
                        )
                        StatusBadge(
                            text = "اتصال آمن",
                            icon = androidx.compose.material.icons.Icons.Outlined.Security,
                            statusColor = if (isVerified || isNormal) Color(0xFF00C853) else Color.Gray
                        )
                    }"""

new_badges = """                    // Badges Row
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(4.dp, Alignment.CenterHorizontally),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        StatusBadge(
                            text = if (isCloudflare) "جاري التحقق" else "تم التحقق",
                            icon = androidx.compose.material.icons.Icons.Outlined.CheckCircle,
                            statusColor = activeColor,
                            modifier = Modifier.weight(1f)
                        )
                        StatusBadge(
                            text = "تحديث البيانات",
                            icon = androidx.compose.material.icons.Icons.Outlined.Sync,
                            statusColor = activeColor,
                            modifier = Modifier.weight(1f)
                        )
                        StatusBadge(
                            text = "اتصال آمن",
                            icon = androidx.compose.material.icons.Icons.Outlined.Security,
                            statusColor = if (isVerified || isNormal) Color(0xFF00C853) else Color.Gray,
                            modifier = Modifier.weight(1f)
                        )
                    }"""

old_badge_fun = """@Composable
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

new_badge_fun = """@Composable
fun StatusBadge(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, statusColor: Color, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .clip(RoundedCornerShape(14.dp))
            .background(Color(0xFF19191C))
            .border(1.dp, Color(0xFF2C2C2E), RoundedCornerShape(14.dp))
            .padding(horizontal = 4.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.Center
    ) {
        Icon(icon, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(12.dp))
        Spacer(modifier = Modifier.width(2.dp))
        Text(text, color = Color.LightGray, fontSize = 9.sp, maxLines = 1, overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis)
        Spacer(modifier = Modifier.width(2.dp))
        Box(modifier = Modifier.size(6.dp).background(statusColor, CircleShape))
    }
}"""

content = content.replace(old_badges, new_badges)
content = content.replace(old_badge_fun, new_badge_fun)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(content)
print("Patched badges")
