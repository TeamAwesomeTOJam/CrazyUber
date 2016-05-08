import awesomeengine
from awesomeengine import vec2d
from awesomeengine import rectangle


def build_corner_graph():
    e = awesomeengine.get_engine()

    corners = list(e.entity_manager.get_by_tag('corner'))

    for corner in corners:
        corner.next_corners = []
        for direction in map(vec2d.Vec2d, [(0,1), (1,0), (0,-1), (-1,0)]):
            found_corner = find_next_corner(corner, direction)
            if found_corner is not None:
                corner.next_corners.append(found_corner)
        if len(corner.next_corners) == 0:
            print corner.x, corner.y


def find_next_corner(corner, dir):
    r = rectangle.from_entity(corner)

    current_tile = corner

    while True:
        check_rect = rectangle.Rect(current_tile.x + dir.x * current_tile.width, current_tile.y + dir.y * current_tile.height, 2, 2)

        next_tiles = awesomeengine.get_engine().entity_manager.get_in_area('road', check_rect)
        distance = 0
        if len(next_tiles) > 0:
            distance += 1
            next_tile = next_tiles.pop()
            if 'corner' in next_tile.tags and distance > 1:
                return next_tile
            else:
                current_tile = next_tile
        else:
            return None

