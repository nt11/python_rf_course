print("Results")
print("-------")

age = 25
height = 170  # in cm
weight = 70   # in kg

if age >= 18 and age <= 65:
    print("You are of working age.")

if height > 150 and height < 190:
    print("Your height is average.")

if weight >= 50 and weight <= 100:
    print("Your weight is within a common range.")

if (age < 18) or (age > 65):
    print("You are not of typical working age.")

if not (height <= 160):
    print("You are taller than 160 cm.")

if (age > 20 and height >= 180) or (weight > 90):
    print("You might be above average in age, height, or weight.")