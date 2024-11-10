print("Results")
print("-------")

# Without 'with' statement
file = open('example.txt', 'w')
file.write('Hello, World!')
file.close()

# With 'with' statement
with open('example.txt', 'w') as file:
   file.write('Hello, World!')

with open("example.txt", 'r') as file:
   print(file.read())