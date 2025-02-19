# a python autostereogram generator using PIL

import os
import sys
import pygame
import random
import time


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

    pattern_height = 200
    pattern_width = 200

    pattern = make_pattern(pattern_width, pattern_height)

    # save pattern to the disk as a png with the unix epoch time as the filename
    filename = f"pattern_{int(time.time())}.png"
    pygame.image.save(pattern, filename)

    print(f"Pattern saved as {filename}.")


if __name__ == "__main__":
    main()
