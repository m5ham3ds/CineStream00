import os

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Add imports
imports = """import com.example.extensions.ExtensionManager
import com.example.extensions.providers.WitAnimeExtension
"""
if "import com.example.extensions.ExtensionManager" not in content:
    content = content.replace("import android.os.Bundle", imports + "import android.os.Bundle")

# Add init logic
init_logic = """
    super.onCreate(savedInstanceState)
    
    ExtensionManager.init(this)
    ExtensionManager.registerExtension(WitAnimeExtension())
"""
if "ExtensionManager.init" not in content:
    content = content.replace("super.onCreate(savedInstanceState)", init_logic)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
