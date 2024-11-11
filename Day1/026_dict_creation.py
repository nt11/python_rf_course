# 1. Using curly braces (literal syntax)
dict1 = {"name": "Alice", "age": 30, "city": "New York"}
print("Dict 1:", dict1)

# 2. Using the dict() constructor with keyword arguments
dict2 = dict(name="Bob", age=25, city="San Francisco")
print("Dict 2:", dict2)

# 3. Using dict() with a list of tuples
dict3 = dict([("name", "Charlie"), ("age", 35), ("city", "Chicago")])
print("Dict 3:", dict3)

# 4. Using dict() with zip()
keys = ["name", "age", "city"]
values = ["David", 28, "Boston"]
dict4 = dict(zip(keys, values))
print("Dict 4:", dict4)

# 5. Dictionary comprehension
names = ["Eve", "Frank", "Grace"]
ages = [22, 31, 29]
dict5 = {name: age for name, age in zip(names, ages)}
print("Dict 5:", dict5)

# 6. Creating from another dictionary (shallow copy)
dict6 = dict(dict1)
print("Dict 6:", dict6)

# 7. Using fromkeys() method (all values are the same)
dict7 = dict.fromkeys(["name", "age", "city"], "Unknown")
print("Dict 7:", dict7)

# 8. Nested dictionary
dict8 = {
    "person1": {"name": "Helen", "age": 40},
    "person2": {"name": "Ivan", "age": 35}
}
print("Dict 8:", dict8)