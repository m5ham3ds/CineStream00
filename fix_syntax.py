import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Fix 1: AnimatedContent transitionSpec
bad_str = "androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) androidx.compose.animation.togetherWith androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300))"
good_str = "androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)).togetherWith(androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)))"

content = content.replace(bad_str, good_str)

# Fix 2: Check bracket balance
def check_brackets(text):
    count = 0
    for char in text:
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
    return count

balance = check_brackets(content)
print(f"Bracket balance: {balance}")

if balance > 0:
    content += "\n" + "}" * balance

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
