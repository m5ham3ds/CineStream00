import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

# Replace arabseed regex
content = content.replace(
"""var name = items[i].querySelector('span') ? items[i].querySelector('span').innerText.trim() : ('سيرفر ' + (i+1));""",
"""var name = items[i].innerText.trim() || items[i].textContent.trim();
if (!name) { var s = items[i].querySelector('span'); if (s) name = s.innerText.trim(); }
if (!name) name = 'سيرفر ' + (i+1);
"""
)

# Replace egybest regex
content = content.replace(
"""var name = items[i].innerText.replace(/[^\\w\\s\\u0600-\\u06FF]/g, '').trim() || ('سيرفر ' + (i+1));""",
"""var name = items[i].innerText.trim() || items[i].textContent.trim() || ('سيرفر ' + (i+1));"""
)

# Replace general fallback regex
content = content.replace(
"""var name = el.querySelector('span') ? el.querySelector('span').innerText.trim() : el.innerText.trim();
                        name = name.replace(/[^\\w\\s\\u0600-\\u06FF]/g, '').trim() || 'سيرفر ' + (i+1);""",
"""var name = el.innerText.trim() || el.textContent.trim();
                        if (!name) { var s = el.querySelector('span'); if (s) name = s.innerText.trim(); }
                        if (!name) name = 'سيرفر ' + (i+1);"""
)

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(content)

