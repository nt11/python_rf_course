print("Results")
print("-------")
# Basic boolean values
is_sunny = True
is_weekend = False

print(f"Is it sunny? {is_sunny}")
print(f"Is it weekend? {is_weekend}")

# Boolean operators
can_go_to_beach = is_sunny and is_weekend
print(f"Can go to beach? {can_go_to_beach}")  # False

# Comparison operators produce booleans
temperature = 25
is_hot = temperature > 30
is_cold = temperature < 15
is_pleasant = 15 <= temperature <= 30

print(f"\nTemperature is {temperature}°C")
print(f"Is it hot? {is_hot}")        # False
print(f"Is it cold? {is_cold}")      # False
print(f"Is it pleasant? {is_pleasant}")  # True

# Converting different types to boolean
name = "Alice"
empty_text = ""
score = 0
high_score = 100

print("\nBoolean conversions:")
print(f"bool('{name}') = {bool(name)}")           # True
print(f"bool('{empty_text}') = {bool(empty_text)}")# False
print(f"bool({score}) = {bool(score)}")           # False
print(f"bool({high_score}) = {bool(high_score)}") # True

# Using boolean in if-else
if bool(name) and temperature > 20:
    print("\nAlice can go outside, it's warm enough!")
else:
    print("\nBetter stay inside!")