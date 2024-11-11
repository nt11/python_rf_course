from typing import List, Union


def calculate_average(numbers: List[float]) -> float:
    """
    Calculate the average of a list of numbers.
    :param numbers: A list of numers to calculate
    :return: Average of input list
    """
    total: float = sum(numbers)
    count: int = len(numbers)
    return total / count


def process_data(data: List[Union[float, str]]) -> None:
    cleaned_data: List[float] = []
    for item in data:
        if isinstance(item, (int, float)):
            cleaned_data.append(float(item))
        elif isinstance(item, str) and item.replace('_', '.', 1).isdigit():
            cleaned_data.append(float(item))

    average: float = calculate_average(cleaned_data)
    print(f"The average is: {average}")


if __name__ == "__main__":
    print("Results")
    print("-------")
    # This data contains a mix of floats, integers, valid number strings, and an invalid string
    mixed_data: List[Union[float, str]] = [1, 2.5, "3.7", 4, "5", "6.8", "invalid"]
    process_data(mixed_data)