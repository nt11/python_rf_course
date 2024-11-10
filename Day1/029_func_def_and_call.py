def calc_rect_a(length, width):
    area = length * width
    return area


if __name__ == "__main__":
    # Function call with positional arguments
    result1 = calc_rect_a(5, 3)
    print(f"Area of rectangle (5 x 3): {result1}")

    # Function call with keyword arguments
    result2 = calc_rect_a(width=4, length=6)
    print(f"Area of rectangle (6 x 4): {result2}")