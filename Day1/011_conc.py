print("Results")
print("-------")

# List repetition
original = [1, 2, 3]
repeated = original * 3
print(repeated)

# Repeating an empty list
empty_repeated = [] * 5
print(empty_repeated)

# Repeating a list with nested elements
nested = [[0]] * 4
print(nested)

# List concatenation using +
list1 = [1, 2, 3]
list2 = [4, 5, 6]
concatenated = list1 + list2
print(concatenated)

# Concatenating multiple lists
list3 = [7, 8, 9]
multi_concat = list1 + list2 + list3
print(multi_concat)

# In-place concatenation using +=
original = [1, 2, 3]
original += [4, 5]
print(original)

# Concatenating with an empty list
result = [] + [1, 2, 3]
print(result)

# Combining repetition and concatenation
combined = [0, 1] * 3 + [2, 3] * 2
print(combined)