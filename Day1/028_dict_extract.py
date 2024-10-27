print("Results")
print("-------")

# Sample dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "job": "Engineer",
    "hobbies": ["reading", "hiking", "photography"]
}

# 1. Accessing a value using key
name = person["name"]
print("1. Name:", name)

# 2. Safe access using get() (with default value)
salary = person.get("salary", "Not specified")
print("2. Salary:", salary)

# 3. Getting all keys
keys = person.keys()
print("3. All keys:", keys)

# 4. Getting all values
values = person.values()
print("4. All values:", values)

# 5. Getting all key-value pairs as tuples
items = person.items()
print("5. All items:", items)

# 6. Checking if a key exists
if "job" in person:
    print("6. Job:", person["job"])

# 7. Length of the dictionary
dict_length = len(person)
print("7. Number of items in dictionary:", dict_length)

# 8. Unpacking dictionary items
for key, value in person.items():
    print(f"8. {key}: {value}")