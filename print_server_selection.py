with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    print(f"{i+1:03d}: {line}", end='')
