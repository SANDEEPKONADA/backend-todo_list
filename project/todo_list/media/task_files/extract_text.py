import re
import json

# Step 1: Read the binary file
with open("OPUS.db", "rb") as f:
    data = f.read()

# Step 2: Extract human-readable ASCII strings (length >= 4)
strings = re.findall(rb"[ -~]{4,}", data)  # ASCII printable characters

# Step 3: Decode bytes to string
decoded_strings = [s.decode("ascii", errors="ignore") for s in strings]

# Step 4: Try basic key-value formatting
kv_pairs = {}
for i in range(0, len(decoded_strings) - 1, 2):
    key = decoded_strings[i].strip()
    value = decoded_strings[i + 1].strip()
    if key and value:
        kv_pairs[key] = value

# Step 5: Save to JSON
with open("output.json", "w") as out_file:
    json.dump(kv_pairs, out_file, indent=4)

print("Extracted data saved to output.json")

