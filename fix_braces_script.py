with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    text = f.read()

target = """                            if (input && !input.value) {
                                input.value = "${title.replace("'", "\\'")}";
                            var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                            if(btn) btn.click();
                            else if(input.form) input.form.submit();
                            return;
                        }
                    }"""

new_target = """                            if (input && !input.value) {
                                input.value = "${title.replace("'", "\\'")}";
                                var btn = document.querySelector('button[type="submit"], input[type="submit"]');
                                if(btn) btn.click();
                                else if(input.form) input.form.submit();
                                return;
                            }
                        }
                    }"""

text = text.replace(target, new_target)
with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
    f.write(text)
