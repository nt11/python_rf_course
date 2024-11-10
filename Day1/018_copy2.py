print("Results")
print("-------")

orig = [1, [2, 3], 4, 5]
shallow_copy = orig.copy()  # would work as orig[:] as well
shallow_copy[0] = 9  # change an element
shallow_copy[1][0] = 8  # change a mutable element of the nested list
shallow_copy += [38]  # change structure
print("Original:", orig)
print("Shallow copy:", shallow_copy)