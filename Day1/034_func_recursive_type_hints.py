print("Results")
print("-------")

def collatz_steps(n: int, steps: int = 0) -> int:
    if n == 1:
        return steps
    elif n % 2 == 0:
        return collatz_steps(n // 2, steps + 1)
    else:
        return collatz_steps(3 * n + 1, steps + 1)

def print_collatz_steps(num: int) -> None:
    result: int = collatz_steps(num)
    print(f"Number {num} takes {result} steps to reach 1.")

if __name__ == "__main__":
    # Test the function
    test_numbers: list[int] = [6, 7, 27, 19, 871]
    for num in test_numbers:
        print_collatz_steps(num)