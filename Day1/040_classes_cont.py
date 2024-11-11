class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model
        self.speed = 0

    def accelerate(self, amount):
        self.speed += amount
        self.check_speed()

    def check_speed(self):
        if self.speed > 120:
            print(f"Warning: {self.make} {self.model} is exceeding speed limit!")
        else:
            print(f"Current speed of {self.make} {self.model}: {self.speed} km/h")

    def drive(self):
        print(f"Starting the {self.make} {self.model}")
        self.accelerate(50)
        self.accelerate(30)
        self.accelerate(60)




if __name__ == "__main__":
    print("Results")
    print("-------")

    # Create a car instance
    my_car = Car("Toyota", "Corolla")

    # Call the drive method
    my_car.drive()

    # Manually accelerate to demonstrate exceeding speed limit
    print("\nAccelerating further:")
    my_car.accelerate(100)