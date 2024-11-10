# Basic type checks
number = 42
text = "Hello"

# Using type()
print(f"type of {number} is {type(number)}")
print(f"type of {text} is {type(text)}")


# Using isinstance()
print(f"\nIs {number} an integer? {isinstance(number, int)}")
print(f"Is {text} a string? {isinstance(text, str)}")

# Comparing types
print(f"\nIs type of {number} same as int? {type(number) is int}")
print(f"Is type of {text} same as float? {type(text) is float}")

#Using in if
if isinstance(number, int):
    print(f"{number} is an integer.")