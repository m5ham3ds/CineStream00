import re

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "r") as f:
    content = f.read()

pattern = re.compile(r'for \(i in 1\.\.10\) \{\s*Handler\(Looper.getMainLooper\(\)\)\.postDelayed\(\{\s*injectScript\(\)\s*\}, i \* 1500L\)\s*\}\s*\}\s*\}\s*\}\s*\}\s*\},', re.DOTALL)

new_code = """for (i in 1..10) {
                            Handler(Looper.getMainLooper()).postDelayed({
                                injectScript()
                            }, i * 1500L)
                        }
                    }
                }
        },"""

content = pattern.sub(new_code, content)

with open("app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt", "w") as f:
    f.write(content)
