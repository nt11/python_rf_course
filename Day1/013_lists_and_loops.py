print("Results")
print("-------")

# Basic iteration through a list
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)

# Modifying list elements in place
numbers = [1, 2, 3, 4, 5]
for i in range(len(numbers)):
    numbers[i] = numbers[i] * 2
print(numbers)

# Performing operations on each item
scores = [75, 82, 93, 68, 87]
total = 0
for score in scores:
    total += score
average = total / len(scores)
print("Average score", average)

# Using range() to iterate a specific number of times
for i in range(5):
    print("iteration", i)