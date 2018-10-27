"""
A module containing class for map containing all objects
"""

import config


class Map:
    """
    A Generalised class for all level maps
    """
    def __init__(self, columns, rows, map_length):
        """
        Initialises the attributes of map
        """
        self.length = map_length
        self.rows = rows
        self.columns = columns
        self.string_array = [[' ' for _ in range(1, columns + 1)] for _ in range(1, rows + 1)]
        self.object_array = [[0 for _ in range(1, columns + 1)] for _ in range(1, rows + 1)]
        self._left_pointer = [0, ]
        self._right_pointer = [config.COLUMNS, ]
        self.player = ''
        self.checkpoints = []
        self.enemies = []
        self.bridges = []
        self.holes = []
        self.coins = []
        self.control_music = ''

    def increment_left_pointer(self, value=1):
        """
        Increments map left pointer by value
        :param value: value by which left pointer has to be incremented default value 1
        :return:
        """
        self._left_pointer += value

    def increment_right_pointer(self, value=1):
        """
        Increments map right pointer by value
        :param value: value by which right pointer has to be incremented default value 1
        :return:
        """
        self._right_pointer += value
