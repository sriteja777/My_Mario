import os
import level1_map
import config
from motion import Player


class Game:
    def __init__(self, nop):
        if nop > 3:
            print("More than 3 players is not supported.")
            return
        self.num_players = nop
        self.left_pointer = []
        self.right_pointer = []
        self.players = []
        self.maps = []
        rows, columns = self.get_terminal_dimensions()
        self.screen = {'rows': rows, 'columns': columns}
        for _ in range(nop):
            self.maps.append(level1_map.Level1Map(self.screen['rows'], int(self.screen['columns']/nop)))
            self.players.append(Player(self.maps[-1].initial_player_position, config.PLAYER, self.maps[-1].map_array))
        # self.maps[0].view_map()
        self.print_screen()

    def print_screen(self):
        lp = 0
        rp = int(self.screen['columns']/self.num_players)
        combined_list = list([self.maps[x].map_array for x in range(self.num_players)])
        for i in zip(*combined_list):
            for j in i:
                for k in j[lp:rp]:
                    print(k, end='')
            print()
            print('\r', end='')

    @staticmethod
    def get_terminal_dimensions():
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows) - 3, int(columns)




game = Game(3)
