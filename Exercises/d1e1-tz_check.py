def generate_checksum_tz(tz: str) -> str:
    """
    Generates checksum for Israeli TZ from the first 8 digits
    :param tz: First 8 digits
    :return: Last digit
    """
    if len(tz) > 8:
        return None

    mult = [1, 2, 1, 2, 1, 2, 1, 2]
    # prepend zeros to reach length 8
    tz2 = "0" * (8 - len(tz)) + tz
    sum_digits = 0

    for i in range(0, len(tz2)):
        # multiply by multipliers
        mult_digit = mult[i] * int(tz2[i])
        # add sum of digits
        sum_digits += mult_digit // 10 + mult_digit % 10

    # return the last digit
    if sum_digits % 10 == 0:
        return "0"

    return str(10 - sum_digits % 10)

def check_id(tz:str) -> bool:
    """
    Check if the TZ is valid
    :param tz:TZ to check
    :return:True if valid, False if not
    """

    return generate_checksum_tz(tz[:-1]) == tz[-1]


if __name__ == "__main__":
    print("Results")
    print("-------")
    cs = generate_checksum_tz("34232242")
    print(cs)
    print(check_id("342322427"))
    print(check_id("342322437"))

