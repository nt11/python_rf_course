# Produce an example of indexing and slicing for lists
print("Results")
print("-------")

# Indexing
l = ['a', 'b', 'c', 'd', 'e']
print(l[0])
print(l[-1])    # Fixed the syntax error: missing closing bracket
print(l[-2])
print()

# Slicing
l = ['a', 'b', 'c', 'd', 'e']
print(l[1:3])   # Elements from index 1 to 2
print(l[:2])    # Elements from start to index 1
print(l[2:])    # Elements from index 2 to end
print(l[:])     # All elements (creates a copy)
print(l[:-1])   # All elements except the last one
print(l[::2])   # Every second element
print(l[::-1])  # All elements in reverse order