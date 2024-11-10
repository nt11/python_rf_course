print("Results")
print("-------")

# Basic usage: range(stop)
print("Counting from 0 to 4:")
for i in range(5):
   print(i, end=" ")
print()  # New line

# Specifying start and stop: range(start, stop)
print("\nCounting from 2 to 6:")
for i in range(2, 7):
   print(i, end=" ")
print()

# Using step: range(start, stop, step)
print("\nCounting odd numbers from 1 to 10:")
for i in range(1, 11, 2):
    print(i, end=" ")
print()

# Counting backwards
print("\nCounting down from 5 to 1:")
for i in range(5, 0, -1):
   print(i, end=" ")
print()