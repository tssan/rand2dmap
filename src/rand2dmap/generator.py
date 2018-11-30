import os

from rand2dmap.tree import (
    Rect,
    split_tree_of_rectangles,
    SplitRectangleError
)
from rand2dmap.preview import create_preview


DEFAULT_OPTIONS = {
    'padding': 1,
    'min_wall_size': 2,
    'min_walls_ratio': 0.4,
    'min_area_percent': 0.3
}

MAP_WIDTH = 100
MAP_HEIGHT = 100

SPLITS = 5

MAPS_PATH = './.maps'


wrap_rect = Rect(0, 0, MAP_WIDTH, MAP_HEIGHT, DEFAULT_OPTIONS)
tree = None
while tree is None:
    try:
        tree = split_tree_of_rectangles(wrap_rect, SPLITS, DEFAULT_OPTIONS)
    except SplitRectangleError:
        print('.', end='')

MAP_ARRAY = []
for y in range(0, MAP_HEIGHT):
    row = []
    for x in range(0, MAP_WIDTH):
        row.append("0")
    MAP_ARRAY.append(row)


def update_rooms(node):
    if node is None:
        return

    if node.is_leaf:
        room = node.data.room

        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                MAP_ARRAY[y][x] = "1"
    else:
        # create path between leaf's centers (nodes not rooms!)
        l1 = node.left.data
        l2 = node.right.data

        c1 = (l1.x + int(l1.width / 2), l1.y + int(l1.height / 2))
        c2 = (l2.x + int(l2.width / 2), l2.y + int(l2.height / 2))

        if c1[0] == c2[0]:
            x = c1[0]
            for y in range(c1[1], c2[1]):
                MAP_ARRAY[y][x] = "2"
        if c1[1] == c2[1]:
            y = c1[1]
            for x in range(c1[0], c2[0]):
                MAP_ARRAY[y][x] = "2"

    update_rooms(node.left)
    update_rooms(node.right)


update_rooms(tree)

new_map_path = os.path.join(MAPS_PATH, 'sample.map')
with open(new_map_path, 'w') as map_file:
    for r in MAP_ARRAY:
        for t in r:
            map_file.write(t)
        map_file.write('\n')

print('\nSuccess: new map ({}x{}): {}'.format(MAP_WIDTH, MAP_HEIGHT, new_map_path))

create_preview(new_map_path, MAP_WIDTH, MAP_HEIGHT, 2)
