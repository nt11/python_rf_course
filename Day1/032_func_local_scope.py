def calculate_area(length, width):
    area = length * width
    print(f"Inside function: area = {area}")
    return area

if __name__ == "__main__":
    length = 10
    width = 5

    result = calculate_area(length, width)
    print(f"Outside function: result = {result}")

    print(f"Original length: {length}")
    print(f"Original width: {width}")

    # This will raise a NameError
    print(f"Trying to access area: {area}")