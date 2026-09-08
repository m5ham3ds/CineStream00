import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

old_status_msg = """                        val statusMsg = if (isCloudflare) {
                            androidx.compose.ui.text.buildAnnotatedString {
                                withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري التحديث ") }
                                withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFFFF1111))) { append("البيانات") }
                            }
                        } else {
                            androidx.compose.ui.text.buildAnnotatedString {
                                withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري البحث في ") }
                                withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                            }
                        }"""

new_status_msg = """                        val statusMsg = when (bypassStatus) {
                            "CHECKING_CLOUDFLARE" -> {
                                androidx.compose.ui.text.buildAnnotatedString {
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تأمين الاتصال بموقع ") }
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                                }
                            }
                            "CLOUDFLARE" -> {
                                androidx.compose.ui.text.buildAnnotatedString {
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تخطي حماية ") }
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFFFF1111))) { append("Cloudflare") }
                                }
                            }
                            "VERIFIED" -> {
                                androidx.compose.ui.text.buildAnnotatedString {
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("تم التخطي ") }
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append("بنجاح") }
                                }
                            }
                            else -> {
                                androidx.compose.ui.text.buildAnnotatedString {
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color.White)) { append("جاري البحث في ") }
                                    withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
                                }
                            }
                        }"""

content = content.replace(old_status_msg, new_status_msg)

old_subtitle = """                        val subtitleMsg = if (isCloudflare) "الموقع محمي، يرجى استكمال التحقق أدناه" else "يرجى الانتظار قليلاً بينما يتم استخراج السيرفرات..."
                        Text(
                            text = subtitleMsg,"""

new_subtitle = """                        val subtitleMsg = when (bypassStatus) {
                            "CHECKING_CLOUDFLARE" -> "يتم الآن الفحص للتأكد من عدم وجود حماية Cloudflare..."
                            "CLOUDFLARE" -> "الموقع محمي، يرجى استكمال مربع التحقق أدناه للمتابعة."
                            "VERIFIED" -> "يتم الآن الانتقال لجلب السيرفرات..."
                            else -> "يرجى الانتظار قليلاً بينما يتم استخراج السيرفرات..."
                        }
                        Text(
                            text = subtitleMsg,"""

content = content.replace(old_subtitle, new_subtitle)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)

print("UI text fixed.")
