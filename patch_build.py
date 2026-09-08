with open("app/build.gradle.kts", "r") as f:
    content = f.read()

old_block = """dependencies {
  implementation("com.startapp:inapp-sdk:5.1.0")"""

new_block = """dependencies {
  implementation("com.github.darkryh:Cloudflare-Bypass:0.0.5")
  implementation("com.startapp:inapp-sdk:5.1.0")"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("app/build.gradle.kts", "w") as f:
        f.write(content)
    print("Patched build.gradle.kts successfully!")
else:
    print("Could not find block!")
