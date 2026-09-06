import re

def patch_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Pattern for ServerSelectionDialog.kt
    old_code_1 = """                                                    var sName = serverItems[i].name.replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                                    if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                        sName = "سيرفر " + (i+1);
                                                    }
                                                    serverItems[i].name = sName;"""
    new_code_1 = """                                                    var sName = serverItems[i].name.trim();
                                                    if (sName === "") {
                                                        sName = "سيرفر " + (i+1);
                                                    }
                                                    serverItems[i].name = sName;"""
    content = content.replace(old_code_1, new_code_1)

    # Pattern for VideoExtractor.kt
    old_code_2 = """                                            var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                            if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                sName = "سيرفر " + (i+1);
                                            }"""
    new_code_2 = """                                            var sName = serverList[i].innerText.trim();
                                            if (sName === "") {
                                                sName = "سيرفر " + (i+1);
                                            }"""
    content = content.replace(old_code_2, new_code_2)

    with open(filepath, 'w') as f:
        f.write(content)

patch_file('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt')
patch_file('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt')
