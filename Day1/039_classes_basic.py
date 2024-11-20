class Dog:
    def __init__(self, name, age, breed):
        self.name = name
        self.age = age
        self.breed = breed

    def bark(self):
        return f"{self.name} says Woof!"

    def birthday(self):
        self.age += 1
        return f"{self.name} is now {self.age} years old."

if __name__ == "__main__":
    # Creating instances of the Dog class
    buddy = Dog("Buddy", 3, "Golden Retriever")
    max = Dog("Max", 5, "Beagle")

    # Using methods of the Dog class
    print(buddy.bark())
    print(max.birthday())
    print(f"{max.name} is a {max.breed}.")