import pygame as pg
import os
from random import seed


FPS = 240
CELLSIZE = 10
# SCREEN / WINDOW SIZE
WINSIZE = (1400, 940)
# MAZE SIZE
TABLESIZE = (WINSIZE[0], WINSIZE[1] - 0)
LINECOLOR = (218, 0, 0)
LINECOLOR_DEBUG = (218, 0, 0)
ORANGE = (255, 98, 0)
# COLOR_LIGHT = (230, 212, 184)
# COLOR_DARK = (242, 219, 87)
COLOR_LIGHT = (242, 219, 87)
COLOR_DARK = (230, 212, 184)
COLOR_BLUE = (20, 20, 192)
COLOR_RED = (192, 20, 20)
BORDER_WDH = 2

WBIAS_STRAIGHT = 3
WBIAS_MEANDERING = 1
MAZE_IMAGE_FILE = 'maze.png'


# for debbuging, random or same every time
# seed(10)
