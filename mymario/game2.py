import os
import level1_map
import config
from motion import Player


class Game:
    def __init__(self, nop):

        rows, columns = self.get_terminal_dimensions()
        self.screen = {'rows': rows, 'columns': columns}
        if not self.multi_player_support(nop):
            print("Sorry " + str(nop) + " is not supported at present screen aspect ratio.")
            return
        self.num_players = nop
        self.left_pointer = []
        self.right_pointer = []
        self.players = []
        self.maps = []
        print("the ratio is ", columns / nop)
        for _ in range(nop):
            self.maps.append(level1_map.Level1Map(self.screen['rows'], int(self.screen['columns']/nop - 1)))
            self.players.append(Player(self.maps[-1].initial_player_position, config.PLAYER, self.maps[-1].map_array))
        # self.maps[0].view_map()
        self.print_screen()

    def multi_player_support(self, num_of_players):
        """
        Returns whether num_of_players multi playing is supported or not.
        Calculated by the ratio columns/num_of_players. By experimental observations, if the ratio
        is greater than 40, then multi playing is supported else not. (But there are some exceptions
        too, this formula doesn't work well for high terminal sizes.)
        :param num_of_players: Number of players
        :return: True is supported else False
        """
        if self.screen['columns']/num_of_players > 40:
            return True
        else:
            return False

    def print_screen(self):
        lp = 0
        rp = int(self.screen['columns']/self.num_players-1)
        combined_list = list([self.maps[x].map_array for x in range(self.num_players)])
        for i in zip(*combined_list):
            for j in i:
                for k in j[lp:rp]:
                    print(k, end='')
                print(config.LINE,end='')
            print()
            print('\r', end='')

    @staticmethod
    def get_terminal_dimensions():
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows) - 3, int(columns)


game = Game(3)
