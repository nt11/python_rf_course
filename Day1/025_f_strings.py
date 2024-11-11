print("Results")
print("-------")

name = "Alice"
age = 30
print(f"My name is {name} and I'm {age} years old.")

# Simple arithmetic
x = 10
y = 5
print(f"{x} plus {y} equals {x + y}")

# Fibonacci series
fib = [0 for x in range(20)]
fib[0] = 1
fib[1] = 1
for i in range(2, 20):
    fib[i] = fib[i - 1] + fib[i - 2]

for i in range(15, 20):
    print(f"fib[{i}] = {fib[i]:,}")

# Percentage formatting
print(f"6 is {6 / 20:.2%} of 20")

import math
e = math.e
print(f"e = {e:.5f}")
print(f"e**5 = {e**5:.3e}")

print(f"c={299792458:.4e} m/s is the speed of light")