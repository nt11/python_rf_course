import math


def calc_circle_prop(radius):
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference


if __name__ == "__main__":
    # Calling the function and unpacking the returned values
    radius = 5
    A, circ = calc_circle_prop(radius)

    print(f"For a circle with radius {radius}:")
    print(f"Area: {A:.2f}")
    print(f"Circumference: {circ:.2f}")