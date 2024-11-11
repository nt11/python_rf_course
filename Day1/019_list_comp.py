print("Results")
print("-------")

# No list comprehension initialization
my_vec = []
for i in range(5):
    my_vec.append(0)
print("my_vec:", my_vec)

# List comprehension initialization
my_vec = [0 for i in range(5)]
print("my_vec:", my_vec)

# No list comprehension
numbers = [1, 2, 3, 4, 5]
squares = []
for x in numbers:
    squares.append(x**2)
print("squares:", squares)

# List comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers]
print("squares:", squares)

# No list comprehension with condition
evens = []
for x in range(6):
    if x % 2 == 0:
        evens.append(x)
print("evens:", evens)

# List comprehension with condition
evens = [x for x in range(6) if x % 2 == 0]
print("evens:", evens)