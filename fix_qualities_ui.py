import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    content = f.read()

# I will find the end of `} else if (isExtractingQualities) {` and everything until the start of `} else { // Show servers list`
# Wait, let's look at what is after the quality list block.

