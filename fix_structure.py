import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Fix 1: The 'togetherWith'
bad_str = "androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)) togetherWith androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300))"
good_str = "androidx.compose.animation.fadeIn(animationSpec = androidx.compose.animation.core.tween(300)).with(androidx.compose.animation.fadeOut(animationSpec = androidx.compose.animation.core.tween(300)))"
content = content.replace(bad_str, good_str)

# Fix 2: Move the closing brace
# First, remove trailing braces that were added incorrectly
content = content.rstrip("}\n ")

# Now, ensure StatusBadge is properly placed.
# Let's just fix the braces explicitly.
parts = content.split("@Composable\nfun StatusBadge")

if len(parts) == 2:
    # Ensure there is a closing brace before @Composable
    if not parts[0].strip().endswith("}"):
         pass
    
    # Actually, the problem is we are missing a `}` to close ServerSelectionDialog.
    # Where does ServerSelectionDialog end?
    # It should end right before `@Composable fun StatusBadge`
    
    # Let's count braces in parts[0]
    def check_brackets(text):
        count = 0
        for char in text:
            if char == '{':
                count += 1
            elif char == '}':
                count -= 1
        return count
        
    b1 = check_brackets(parts[0])
    print(f"Brackets in part 1: {b1}")
    if b1 > 0:
        parts[0] += "\n" + "}" * b1 + "\n"
        
    b2 = check_brackets("@Composable\nfun StatusBadge" + parts[1])
    print(f"Brackets in part 2: {b2}")
    if b2 > 0:
        parts[1] += "\n" + "}" * b2 + "\n"
        
    content = parts[0] + "@Composable\nfun StatusBadge" + parts[1]

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)

