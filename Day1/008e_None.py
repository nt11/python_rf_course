x = None

# Check the type
print(type(x))  # <class 'NoneType'>

# None evaluates to False in boolean context
print(bool(None))  # False

# Common usage of None
value = None
if value is None:
    print("Value is None")

# Best practice: use 'is' and 'is not' with None
# Don't do this:
print(value == None)  # Works but not recommended

# Do this instead:
print(value is None)  # Correct way

# Multiple variables can point to None
a = None
b = None
print(a is b)  # True - they point to the same object
