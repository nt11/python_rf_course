print("Results")
print("-------")
if __name__ == "__main__":
    try:
        # Code that might raise an exception
        result = 10 / 0
    except ZeroDivisionError:
        # Handle the specific exception
        print("Can't divide by zero!")
    try:
        # Some risky code
        num = int("abc")
    except ValueError:
        print("Invalid number")
    except TypeError:
        print("Type error occurred")
    try:
        # Some risky code
        num = int("abc")
    except Exception:
        print("An error occurred")
