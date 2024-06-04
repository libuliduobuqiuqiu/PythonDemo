"""
    :Date: 2024-5-30
    :Author: linshukai
    :Description: about rectangle and square
"""


class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return f"Rectangle(width={self.width}, height={self.height})"

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * self.width + 2 * self.height

    def get_diagonal(self):
        return (self.width**2 + self.height**2) ** 0.5

    def get_picture(self):
        if self.width > 50 or self.height > 50:
            return "Too big for picture."

        output = []
        for _ in range(self.height):
            output.append(self.width * "*")
        return "\n".join(output)

    def get_amount_inside(self, obj):
        if obj.width == obj.height:
            return (self.width // obj.width) * (self.height // obj.height)
        else:
            tmp1 = (self.width // obj.width) * (self.height // obj.height)
            tmp2 = (self.width // obj.height) * (self.height // obj.width)
            return tmp1 if tmp1 > tmp2 else tmp2


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def __eq__(self, other):
        if "Square" in self.__str__() and "Square" in other.__str__():
            return True
        if "Rectangle" in self.__str__() and "Rectangle" in other.__str__():
            return True
        return False

    def set_side(self, side):
        self.width = side
        self.height = side

    def __str__(self):
        if self.width == self.height:
            return f"Square(side={self.width})"
        else:
            return super().__str__()


if __name__ == "__main__":
    rect = Rectangle(3, 6)
    print(rect.get_area())
    print(rect.set_width(7))
    print(rect.set_height(3))
    print(rect.get_perimeter())
    print(rect)
    print(rect.get_picture())

    sq = Square(9)
    print(sq.get_area())
    sq.set_side(4)
    print(sq.get_diagonal())
    print(sq)
    print(sq.get_picture())

    rect.set_height(8)
    rect.set_width(16)
    print(rect.get_amount_inside(sq))
