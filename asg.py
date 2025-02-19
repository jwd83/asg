# a python autostereogram generator using PIL

import os
import sys
import pygame
import random
import time
from print_color import print_color


def make_pattern(width, height):
    # make a pygame surface with a random grayscale pattern
    pattern = pygame.Surface((width, height))
    for y in range(height):
        for x in range(width):
            gray_intensity = random.randint(0, 255)

            pattern.set_at((x, y), (gray_intensity, gray_intensity, gray_intensity))

    return pattern


def main():
    pygame.init()

    # check if we were provided a path to the depth file
    if len(sys.argv) < 2:

        print_color(
            "RED",
            "ERROR: No depth map file was specified.\nUsage: python asg.py <depthmap.png>",
        )
        sys.exit(1)

    pattern_height = 256
    pattern_width = 256

    pattern = make_pattern(pattern_width, pattern_height)

    # save pattern to the disk as a png with the unix epoch time as the filename
    filename = f"pattern_{int(time.time())}.png"
    pygame.image.save(pattern, filename)

    print_color("GREEN", f"Pattern saved as {filename}.")

    depth_map = pygame.image.load(sys.argv[1]).convert()
    depth_map_width, depth_map_height = depth_map.get_size()


if __name__ == "__main__":
    main()
