print("Results")
print("-------")

p1 = [1, [2, 3], 4]
p_copy = p1
p_copy[0] = 5
p_copy[1][0] = 17
print("p1 =", p1)
print("p_copy =", p_copy)

import copy
p2 = [1, [2, 3], 4]
p2_deep = copy.deepcopy(p2)
p2[0] = 5
p2[1][0] = 17
print("p2 =", p2)
print("p2_deep =", p2_deep)