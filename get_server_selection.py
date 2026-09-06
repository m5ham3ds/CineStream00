with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    text = f.read()

import re
print(re.search(r'if \(isLoading && !isFailed\) \{.*?(?=if \(isExtractingQuality)', text, flags=re.DOTALL).group(0))
