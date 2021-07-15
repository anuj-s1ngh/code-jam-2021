# This code is adapted from http://www.roguebasin.com/index.php/Raycasting_in_python by init. initd5@gmail.com

from typing import List, Callable, Tuple, Union
from math import sin, cos

char_wh_ratio = 0.5


def raycast(level_layout: List[str], x: int, y: int, opaque: str, light_func: Callable[[str, int], str], invisible_char: str = '?',
            steps: int = 360, fov: int = 360) -> List[str]:
    """
    Takes in a level_layout and filters out all the things that aren't visible to the player.

    It works like this:
    We start at the player's coordinates and cast [fov / step] rays, one for each heading.\
    Each ray travels in a certain heading by adding cos(heading) to x and sin(heading) to y repeatedly
    until it hits an opaque tile.
    Each tile a ray lands is set as visible.

    :param level_layout: A list of strings, where each string is a line in the entire level layout.
    :param x: x position of origin
    :param y: y position of origin
    :param opaque: A string containing all the characters that block vision/light.
    :param light_func: A function that takes in a character and its distance from the light source,
        and outputs a string based upon those parameters.
    :param invisible_char: The character used to mark an invisible spot.
    :param step: Number of degrees between each casted ray. Increase the number for speed, lower for accuracy.
        Must be in the range 1 - fov (recommended absolute max like 10-15).
    :param fov: Angle of vision that player can see (going clockwise starting from the right). DON'T CHANGE

    :return: A list of strings with the same dimensions as the inputted level_layout,
        except only the visible stuff remains
    """

    width = len(level_layout[0])
    height = len(level_layout)
    return_layout = [[invisible_char for _ in line] for line in level_layout]
    # list of visible tiles, each represented by a tuple containing: (x, y, dist_from_origin, char)
    visible_tiles: List[Tuple[int, int, Union[float, int]]] = [(x, y, 0)]

    # speed up tactics
    min_dist = min(x, y, width - x, height - y)  # dunno speed of bools, maybe unnecessary

    head_to_angle = fov / steps
    for heading in range(steps):
        heading *= head_to_angle
        # starting point
        ray_x = x
        ray_y = y

        # get amount of x and y delta using trig to make the absolute delta 1 in the specified heading (i)
        dx = cos(heading)  # actually not that slow. in fact, its faster for sub-decimal values of heading
        dy = sin(heading) * char_wh_ratio # due to the amount of time rounding takes. even with int(), it's roughly 40-50% slower

        for dist in range(1, max(width, height)):  # Cast the ray
            ray_x += dx
            ray_y += dy
            rx, ry = round(ray_x), round(ray_y)

            if dist >= min_dist:
                if ry < 0 or ry >= height or rx < 0 or rx >= width:  # Break if ray is out of bounds
                    break

            visible_tiles.append((rx, ry, dist))  # Make tile visible
            # todo make a way for different light levels (and colors maybe) to come and combine together
            #  maybe use a metric to measure light level instead of directly going for the char
            #  maybe abandon light_func and just do inv sqrt (as it is irl). take in light intensity/color instead
            #  maybe use a unit of dist not 1? altho idk. prob not

            if level_layout[ry][rx] in opaque:  # Stop on opaque tile
                break

    for tile in visible_tiles:
        return_layout[tile[1]][tile[0]] = light_func(level_layout[tile[1]][tile[0]], tile[2])
    return [''.join(line) for line in return_layout]


if __name__ == '__main__':
    from sprites import maps
    from lighting import light_dark_chars2 as ldc
    from time import time
    from os import get_terminal_size as gts

    ts = gts()
    s = ['#' * ts.columns] * ts.lines

    t = time()
    n = 10
    for i in range(20):
        display = raycast(s, ts.columns // 2, ts.lines // 2, 'o', lambda a, b: ldc[min(len(ldc)-1, b)], steps=360 * 4)
        for line in display:
            ...  # print(line)
    print('fps: ', n / (time() - t))
