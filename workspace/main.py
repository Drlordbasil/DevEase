import math

class DevEase:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

def calculate_sum_of_squares(numbers):
    return sum([x**2 for x in numbers])

def main():
    name = input("Enter your name: ")
    dev_ease = DevEase(name)
    greeting = dev_ease.greet()
    print(greeting)

    numbers = [1, 2, 3, 4, 5]
    sum_of_squares = calculate_sum_of_squares(numbers)
    print(f"The sum of squares is: {sum_of_squares}")

if __name__ == "__main__":
    main()
