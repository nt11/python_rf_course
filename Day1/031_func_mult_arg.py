def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"

def power(base, exponent=2):
    return base ** exponent

if __name__ == "__main__":
    # Examples using the greet function
    print(greet("Alice"))
    print(greet("Bob", greeting="Hi"))
    print(greet("Charlie", greeting="Hey", punctuation="..."))
    print(greet("David", punctuation="?"))

    # Examples using the power function
    print(power(5))
    print(power(2, 3))
    print(power(exponent=3, base=2))