import yaml

def print_yaml_with_types(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print(' ' * indent + f"{key}: ({type(value).__name__})")
            print_yaml_with_types(value, indent + 2)
    elif isinstance(data, list):
        print(' ' * indent + f"(list of {len(data)} items)")
        for item in data:
            print_yaml_with_types(item, indent + 2)
    else:
        print(' ' * indent + f"({type(data).__name__}) {data}")

# Read the YAML file
with open('rf_setup.yaml', 'r') as file:
    data = yaml.safe_load(file)

# Print the original data with types
print("Original data with types:")
print_yaml_with_types(data)

# Modify the data
data['equipment']['signal_generator']['output_power'] = 15
data['measurement_points'].append({'frequency': 10e9, 'power': 0})
data['settings']['averaging'] = 20

# Print the modified data with types
print("\nModified data with types:")
print_yaml_with_types(data)

# Write the modified data back to a new YAML file
with open('rf_setup_modified.yaml', 'w') as file:
    yaml.dump(data, file, default_flow_style=False)

print("\nModified data has been written to 'rf_setup_modified.yaml'")

# Read and print the contents of the new file
with open('rf_setup_modified.yaml', 'r') as file:
    print("\nContents of 'rf_setup_modified.yaml':")
    print(file.read())