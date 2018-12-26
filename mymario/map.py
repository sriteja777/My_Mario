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
    def __init__(self, map_id, columns, rows, map_length):
        """
        Initialises the attributes of map
        """
        self.id = id
        self.length = map_length
        self.rows = rows
        self.columns = columns
        self.map_array = [[' ' for _ in range(1, self.length + 1)] for _ in range(1, self.rows + 1)]
        self.object_array = [[0 for _ in range(1, self.length + 1)] for _ in range(1, self.rows + 1)]
        self.left_pointer = 0
        self.right_pointer = self.columns
        self.foreground = []
        self.background = []
        self.checkpoints = []
        self.enemies = []
        self.bridges = []
        self.holes = []
        self.coins = []
        self.control_music = ''

    def view_map(self, reverse=False):
        flag = 1
        lp = 0
        rp = self.columns

        if reverse:
            flag = -1
            rp = self.length
            lp = self.length - self.columns

        # for i in self.map_array[:]:
        #     for j in i[lp:rp]:
        #         print(j, end='')
        #     print()
        #     print('\r', end='')

        while True:
            os.system('tput reset')
            for i in self.map_array[:]:
                for j in i[lp:rp]:
                    print(j, end='')
                print()
                print('\r', end='')
            if rp > self.length or lp < 0:
                break

            lp += flag
            rp += flag
            sleep(0.05)

    # def remove_obj(self, ):
