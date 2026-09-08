import os
import json

transcript_path = ".aistudio/artifacts/brain/54881797-f2b1-4f90-8832-994aeb0ca1bc/.system_generated/logs/transcript.jsonl"
if not os.path.exists(transcript_path):
    print("Transcript not found")
    exit(0)

found = []
with open(transcript_path, 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if 'egydead' in line.lower() and ('class=' in line.lower() or 'href=' in line.lower()):
            found.append(line[:500])

for f in found[-10:]:
    print(f)
    print("-" * 40)
