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
    pygame.display.set_mode((400, 400))

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
    print_color("GREEN", f"Depth map size: {depth_map_width}x{depth_map_height}")

    pattern_depth_ratio = depth_map_width / pattern_width
    print_color("GREEN", f"Pattern depth ratio: {pattern_depth_ratio}")

    # make a pattern map that is the base pattern repeated across the depth map
    pattern_map = pygame.Surface((depth_map_width, depth_map_height))
    for y in range(depth_map_height):
        for x in range(depth_map_width):
            pattern_map.set_at(
                (x, y), pattern.get_at((x % pattern_width, y % pattern_height))
            )

    projection_map = pygame.Surface((depth_map_width, depth_map_height))
    projection_map.fill((255, 0, 0))

    # create the stereogram projection by shifting pixels by the depth data in the pattern
    for x in range(depth_map_width):
        for y in range(depth_map_height):
            # the first pattern_width pixels are the unaltered. maybe we should offset make the projection wider by the pattern offset to account for this.
            if x < pattern_width:
                projection_map.set_at((x, y), pattern_map.get_at((x, y)))
            else:
                shift = depth_map.get_at((x, y))[0] / pattern_depth_ratio
                projection_map.set_at((x, y), pattern_map.get_at((x - int(shift), y)))

    # save the projection map to the disk
    projection_filename = f"projection_{int(time.time())}.png"
    pygame.image.save(projection_map, projection_filename)
    print_color("GREEN", f"Projection map saved as {projection_filename}.")

    # change the window size to match the depth map
    pygame.display.set_mode((depth_map_width, depth_map_height))

    screen = pygame.display.get_surface()

    state = 0

    while True:

        state = state % 3

        # clear the screen
        screen.fill((0, 0, 0))

        if state == 0:
            screen.blit(depth_map, (0, 0))
        elif state == 1:
            screen.blit(pattern_map, (0, 0))
        elif state == 2:
            screen.blit(projection_map, (0, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            # check for a mouse click to change the state
            if event.type == pygame.MOUSEBUTTONDOWN:
                state += 1

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)


if __name__ == "__main__":
    main()
