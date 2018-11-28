from random import randint


class Node:
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    @property
    def is_leaf(self):
        return self.left is None and self.right is None


class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self._room = None

    @property
    def room(self):
        if self._room is None:
            self._room = self.create_room()
        return self._room

    def create_room(self):
        x = randint(self.x, self.x + int(self.width / 2))
        y = randint(self.y, self.y + int(self.height / 2))
        width = abs(x - randint(x, self.x + self.width))
        height = abs(y - randint(y, self.y + self.height))

        return Rect(x, y, width, height)


def split_rect(rect):
    if randint(0, 1) == 0:  # split vertical
        r1 = Rect(
            rect.x, rect.y,
            randint(1, rect.width), rect.height
        )
        r2 = Rect(
            rect.x + r1.width, rect.y,
            rect.width - r1.width, rect.height
        )
    else:  # split horizontal
        r1 = Rect(
            rect.x, rect.y,
            rect.width, randint(1, rect.height)
        )
        r2 = Rect(
            rect.x, rect.y + r1.height,
            rect.width, rect.height - r1.height
        )
    return r1, r2


def split_tree_of_rectangles(rect, step):
    tree = Node(rect)
    if step != 0:
        split = split_rect(rect)
        if split:
            tree.left = split_tree_of_rectangles(split[0], step - 1)
            tree.right = split_tree_of_rectangles(split[1], step - 1)
    return tree
