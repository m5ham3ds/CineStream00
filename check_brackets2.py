def check_brackets(filepath):
    with open(filepath, "r") as f:
        content = f.read()
    
    count = 0
    for i, char in enumerate(content):
        if char == '{':
            count += 1
        elif char == '}':
            count -= 1
            if count == 0 and i < len(content) - 100:
                print(f"Balance dropped to 0 at index {i}. Context around it:")
                print(content[i-50:i+50])
                
check_brackets2 = check_brackets("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt")
