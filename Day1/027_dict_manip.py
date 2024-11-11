print("Results")
print("-------")

# Start with a sample dictionary
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
print("Original dictionary:", my_dict)

# Adding/updating a single key-value pair
my_dict["job"] = "Engineer"
print("After adding 'job':", my_dict)

# Updating an existing value
my_dict["age"] = 31
print("After updating 'age':", my_dict)

# Removing a key-value pair
del my_dict["city"]
print("After deleting 'city':", my_dict)

# Updating multiple key-value pairs
my_dict.update({"salary": 75000, "department": "IT"})
print("After updating multiple values:", my_dict)

# Clearing all items from the dictionary
my_dict.clear()
print("After clearing:", my_dict)