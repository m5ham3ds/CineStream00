with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    text = f.read()

def count_braces(s):
    open_b = s.count('{')
    close_b = s.count('}')
    return open_b, close_b

print(count_braces(text))
