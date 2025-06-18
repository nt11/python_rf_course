print("Results")
print("-------")

class MyError(Exception):
    pass

if __name__=="__main__":
    try:
        # some code
        raise ValueError("Original Error")
    except ValueError as e:
        print(f"Handling error {e}")
          # Re-raises the last exception

    try:
        # some code
        raise MyError("Custom Error")
    except ValueError as e:
        print (f"ValueError {e}")
    except Exception as e:
        print(f"Handling error {e}")
