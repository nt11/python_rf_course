import re  # Import the re module for regular expressions to detect scientific notation numbers

import yaml  # Import the PyYAML module for reading and writing YAML files

# Regular expression to detect scientific notation numbers in strings
scientific_notation_re = re.compile(r"^-?\d+(\.\d+)?[eE]-?\d+$")

# Custom function to convert scientific notation strings to float
def scientific_notation_constructor(loader, node):
    value = loader.construct_scalar(node)
    if scientific_notation_re.match(value):
        try:
            return float(value)
        except ValueError:
            pass
    return value

def print_yaml_with_types(data, indent=0):
    """
    Print the YAML data with types of the values.
    Calls itself recursively to print nested dictionaries and lists.
    :param data:
    :param indent:
    :return:
    """
    if isinstance(data, dict):
        for key, value in data.items():
            # if the value is a dictionary or a list, print the key and its type
            # and then recursively call the function to print the value
            # with an increased indent
            # otherwise, print the key, the type of the value, and the value
            if isinstance(value, (dict, list)):
                print(' ' * indent + f"{key}: ({type(value).__name__})")
                print_yaml_with_types(value, indent + 4)
            else:
                print(' ' * indent + f"{key}: ({type(value).__name__}) {value}")
    elif isinstance(data, list):
        print(' ' * indent + f"(list of {len(data)} items)")
        for item in data:
            print_yaml_with_types(item, indent + 4)
    else:
        print(' ' * indent + f"({type(data).__name__}) {data}")

if __name__ == '__main__':
    # Register the custom constructor for strings in SafeLoader to
    # convert scientific notation to float
    yaml.SafeLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_SCALAR_TAG,
                                    scientific_notation_constructor    )

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

    # Write the modified data back to a new YAML file
    with open('rf_setup_modified.yaml', 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    print("\nModified data has been written to 'rf_setup_modified.yaml'")

    # Read and print the contents of the new file
    with open('rf_setup_modified.yaml', 'r') as file:
        data = yaml.safe_load(file)

    # Print the modified data with types
    print("\nModified data with types:")
    print_yaml_with_types(data)
