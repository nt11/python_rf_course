print("Results")
print("-------")

def modify_list(lst):
    print(f"Inside function, initially: {lst}")
    lst[0] = 17
    lst.append(4)
    print(f"Inside function, after modification: {lst}")

def modify_number(num):
    print(f"Inside function, initially: {num}")
    num += 1
    print(f"Inside function, after modification: {num}")

if __name__ == "__main__":
    # Example with a mutable object (list)
    my_list = [1, 2, 3]
    print(f"Before function call: {my_list}")
    modify_list(my_list)
    print(f"After function call: {my_list}")

    print("\n" + "=" * 40 + "\n")

    # Example with an immutable object (integer)
    my_number = 42
    print(f"Before function call: {my_number}")
    modify_number(my_number)
    print(f"After function call: {my_number}")

    # Example with a mutable object (list)
    my_list = [1, 2, 3]
    print(f"Before function call: {my_list}")
    modify_list(my_list)
    print(f"After function call: {my_list}")