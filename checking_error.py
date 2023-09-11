from maze_settings import *
import sys


class ErrorHandler:
    def __init__(self):
        pass

    def value_check(self):
        try:
            if WINSIZE[0] % CELLSIZE != 0:
                raise ValueError(
                    '\"MAZE WIDTH\" MUST BE DIVISIBLE WITH \"CELL SIZE\"!')
            if TABLESIZE[1] % CELLSIZE != 0:
                raise ValueError(
                    '\"MAZE HEIGHT\" MUST BE DIVISIBLE WITH \"CELL SIZE\"!')
        except Exception as error:
            print('Caught this error: ' + repr(error))
            sys.exit()
