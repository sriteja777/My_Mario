import os
import level1_map
import config
from time import sleep


class Game:
    def __init__(self, nop):
        self.num_players = nop
        self.left_pointer = []
        self.right_pointer = []
        self.players = []
        self.maps = []
        rows, columns = self.get_terminal_dimensions()
        self.screen = {'rows': rows, 'columns': columns}
        self.maps.append(level1_map.Level1Map(self.screen['rows'], self.screen['columns']))

    @staticmethod
    def get_terminal_dimensions():
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows) - 3, int(columns)


game = Game(1)
