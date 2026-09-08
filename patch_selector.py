with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_selector = "var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type=\"checkbox\"], #challenge-form, .mark-as-human');"
new_selector = "var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, #challenge-form, .mark-as-human');"

if old_selector in content:
    content = content.replace(old_selector, new_selector)
    with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
        f.write(content)
    print("Patched SiteScripts.kt successfully!")
else:
    print("Could not find selector block!")
