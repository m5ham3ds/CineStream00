with open("settings.gradle.kts", "r") as f:
    content = f.read()

old_block = """dependencyResolutionManagement {
  repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
  repositories {
    google()
    mavenCentral()
  }
}"""

new_block = """dependencyResolutionManagement {
  repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
  repositories {
    google()
    mavenCentral()
    maven { url = uri("https://jitpack.io") }
  }
}"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open("settings.gradle.kts", "w") as f:
        f.write(content)
    print("Patched successfully!")
else:
    print("Could not find block!")
