"""
A module containing class for map containing all objects
"""

import config
import os
from time import sleep


class Map:
    """
    A Generalised class for all level maps
    """
    def __init__(self, columns, rows, map_length, player_position):
        """
        Initialises the attributes of map
        """
        self.length = map_length
        self.rows = rows
        self.columns = columns
        self.string_array = [[' ' for _ in range(1, columns + 1)] for _ in range(1, rows + 1)]
        self.object_array = [[0 for _ in range(1, columns + 1)] for _ in range(1, rows + 1)]
        self.foreground = []
        self.background = []
        self.checkpoints = []
        self.enemies = []
        self.bridges = []
        self.holes = []
        self.coins = []
        self.control_music = ''
        self.initial_position = player_position

    def view_map(self, reverse=False):
        flag = 1
        lp = 0
        rp = self.columns

        if reverse:
            flag = -1
            rp = self.length
            lp = self.length - self.columns

        while True:
            os.system('tput reset')
            for i in config.DIMENSIONAL_ARRAY[:]:
                for j in i[lp:rp]:
                    print(j, end='')
                print()
                print('\r', end='')
            if rp > self.length or lp < 0:
                break

            lp += flag
            rp += flag
            sleep(0.05)
