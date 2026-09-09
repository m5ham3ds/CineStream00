def check_brackets(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    count = 0
    for i, char in enumerate(content):
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
            if count < 0:
                print(f"Negative balance at {i}")
                
    print(f"Final balance: {count}")

check_brackets("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt")
