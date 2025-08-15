class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        return f"{self.feet} feet {self.inches} inches"

    def __lt__(self, other):
        return (self.feet * 12 + self.inches) < (other.feet * 12 + other.inches)

    def __le__(self, other):
        return (self.feet * 12 + self.inches) <= (other.feet * 12 + other.inches)

    def __eq__(self, other):
        return (self.feet * 12 + self.inches) == (other.feet * 12 + other.inches)

    def __gt__(self, other):
        return (self.feet * 12 + self.inches) > (other.feet * 12 + other.inches)

    def __ge__(self, other):
        return (self.feet * 12 + self.inches) >= (other.feet * 12 + other.inches)

    def __ne__(self, other):
        return (self.feet * 12 + self.inches) != (other.feet * 12 + other.inches)


height_1 = Height(4, 5)
height_2 = Height(4, 5)
height_3 = Height(4, 6)
height_4 = Height(5, 10)
height_5 = Height(5, 10)
height_6 = Height(5, 9)

# Put them in a list
heights = [height_1, height_2, height_3, height_4, height_5, height_6]

# Sort them (this uses your __lt__ method)
sorted_heights = sorted(heights)

for h in sorted_heights:
    print(h)

print(height_1 < height_3)  # returns true
print(height_1 <= height_2)  # returns true
print(height_4 == height_5)  # returns true
print(height_3 > height_2)  # returns true
print(height_1 >= height_2)  # returns true
print(height_5 != height_6)  # returns true
