with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_status = """                    val statusMsg = if (isVerified) {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("عملية تحديث البيانات ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append("نجحت!") }
                        }
                    } else if (isNormal) {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري الفحص في ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                        }
                    } else {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري عملية ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFFFF1111))) { append("تحديث البيانات...") }
                        }
                    }"""

new_status = """                    val statusMsg = if (isVerified) {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تم الاتصال ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append("بنجاح!") }
                        }
                    } else {
                        androidx.compose.ui.text.buildAnnotatedString {
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("البحث في ") }
                            withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                        }
                    }"""

content = content.replace(old_status, new_status)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
