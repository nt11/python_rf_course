print("Results")
print("-------")

# int(): Convert a string or float to an integer
print("int():")
print(int("123"))  # String to int
print(int(45.67))  # Float to int
print(int("-789"))  # Negative string to int
print()

# abs(): Return the absolute value of a number
print("abs():")
print(abs(-10))
print(abs(10))
print()

# divmod(): Return quotient and remainder of division
print("divmod():")
print(divmod(20, 3))  # (quotient, remainder)
print(divmod(-20, 3))  # Note the behavior with negative numbers
print()

# pow(): Raise a number to a power
print("pow():")
print(pow(2, 3))  # 2^3
print(pow(2, 3, 5))  # (2^3) % 5 (with modulus)
print()