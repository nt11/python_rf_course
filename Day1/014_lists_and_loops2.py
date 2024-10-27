print("Results")
print("-------")

# Using enumerate() to access index and value
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits):
    print("Index", index, fruit)

# Nested for loops with a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
for row in matrix:
    for item in row:
        print(item, end=' ')
    print()  # New line after each row

# Modifying the original list (demonstrating reference behavior)
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num % 2 == 0:
        numbers.remove(num)
print(numbers)  # Note: This can lead to unexpected results