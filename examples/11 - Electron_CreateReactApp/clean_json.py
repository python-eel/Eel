import json

# Read the JSON file
with open('package.json', 'r') as file:
    data = json.load(file)

# Remove unwanted keys from the data
keys_to_remove = ["private", "dependencies", "scripts", "eslintConfig", "browserslist", "devDependencies"]

for key in keys_to_remove:
    if key in data:
        del data[key]

# Write the modified data back to the JSON file
with open('build/package.json', 'w') as file:
    json.dump(data, file, indent=4)