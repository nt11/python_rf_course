# 1. Creating tuples
empty_tuple = (); point = (3, 4); rgb_color = (255, 128, 0); person = ("Alice", 25)

# 2. Accessing tuple elements (indexing)
x_coordinate = point[0]; y_coordinate = point[1]
print(f"Coordinates: {x_coordinate}, {y_coordinate}")

# 3. Tuple unpacking
r, g, b = rgb_color; name, age = person
print(f"RGB: {r}, {g}, {b}"); print(f"Person: {name} is {age}")

# 4. Multiple assignment with tuples
a, b = 1, 2; c, d = b, a  # Swapping values: c=2, d=1

# 5. Tuple comparison
point1, point2, point3 = (1, 2), (1, 3), (1, 2)
print(f"point1 == point2: {point1 == point2}, point1 < point2: {point1 < point2}")

# 6. Nested tuples
matrix = ((1, 2, 3), (4, 5, 6))
print(f"First element: {matrix[0][0]}, Last element: {matrix[1][2]}")

# 7. Tuple with single element (note the comma)
single_tuple, not_tuple = (42,), (42)
print(f"Types: {type(single_tuple)}, {type(not_tuple)}")

# 8. Basic tuple operations
tuple1, tuple2 = (1, 2, 3), (4, 5, 6)
print(f"Combined: {tuple1 + tuple2}, Repeated: {tuple1 * 2}")

# 9. Length of a tuple
point_3d = (1, 2, 3); print(f"Length: {len(point_3d)}")

# 10. Checking if element exists
print(f"Has 3? {3 in point_3d}, Has 6? {6 in point_3d}")