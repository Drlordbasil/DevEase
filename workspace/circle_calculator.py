import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def circumference(self):
        return 2 * math.pi * self.radius

def main():
    radius = float(input("Enter the radius of the circle: "))
    circle = Circle(radius)
    print("Area:", circle.area())
    print("Circumference:", circle.circumference())

if __name__ == "__main__":
    main()

import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def circumference(self):
        return 2 * math.pi * self.radius

def main():
    radius = float(input("Enter the radius of the circle: "))
    circle = Circle(radius)
    print("Area:", circle.area())
    print("Circumference:", circle.circumference())

if __name__ == "__main__":
    main()
