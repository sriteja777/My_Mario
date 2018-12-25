import os
from random import randrange
from threading import Thread
from time import sleep

import keyboard

import level1_map
import config
from controls import Controls
from motion import Player
from objects import Obj

inc = 0


class Game:
    def __init__(self, nop):

        rows, columns = self.get_terminal_dimensions()
        self.screen = {'rows': rows, 'columns': columns}
        if not self.multi_player_support(nop):
            print("Sorry " + str(nop) + " is not supported at present screen aspect ratio.")
            return
        self.initialise_screen()
        self.num_players = nop
        self.left_pointer = []
        self.right_pointer = []
        self.players = []
        self.maps = []
        print("the ratio is ", columns / nop)
        for _ in range(nop):
            self.maps.append(level1_map.Level1Map(self.screen['rows'], int(self.screen['columns']/nop - 1)))
            self.players.append(Player(self.maps[-1].initial_player_position, config.PLAYER, self.maps[-1].map_array))
            self.left_pointer.append(0)
            self.right_pointer.append(self.maps[-1].columns)
        self.controls = Controls()
        # self.maps[0].view_map()
        self.print_screen()

        for player_id in range(self.num_players):
            inp_thread = Thread(target=self.get_input_for_player, args=(player_id,))
            inp_thread.daemon = True
            inp_thread.start()

        while True:
            try:
                if config.stop.is_set() or config.timeout.is_set():
                    break
                sleep(0.1)
                [ self.make_updates(x) for x in range(self.num_players) ]
                self.updates()

            except KeyboardInterrupt:
                break

    def get_input_for_player(self, player_id):
        while True:
            import sys
            import tty
            import termios
            file_desc = sys.stdin.fileno()
            old_settings = termios.tcgetattr(file_desc)
            try:
                tty.setraw(sys.stdin.fileno())
                sleep(0.07)
                self.move_player(player_id)
            finally:
                termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)

    def move_player(self, player_id):
        if keyboard.is_pressed(self.controls.player[player_id].LEFT):
            self.players[player_id].move_left()
        if keyboard.is_pressed(self.controls.player[player_id].UP):
            self.players[player_id].move_up()
        if keyboard.is_pressed(self.controls.player[player_id].RIGHT):
            self.players[player_id].move_right()
        if keyboard.is_pressed(self.controls.player[player_id].UP_RIGHT):
            self.players[player_id].move_up_right()
        if keyboard.is_pressed(self.controls.player[player_id].UP_LEFT):
            self.players[player_id].move_up_left()

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

    def initialise_screen(self):
        Obj(self.screen['columns'], self.screen['rows'], 1, 3, ' ')

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

    def make_updates(self, x):
        """
        Make updates and prints the map to the terminal
        :return:
        """
        global inc

        rand_x = randrange(1, 100)
        rand_x_2 = randrange(1, 150)
        rand_x_3 = randrange(1, 75)
        if inc % rand_x == 0:
            self.maps[x].clouds[0].move_cloud()
        if inc % rand_x_2 == 0:
            self.maps[x].clouds[1].move_cloud()
        if inc % rand_x_3 == 0:
            self.maps[x].clouds[2].move_cloud()
        inc += 1

    def updates(self):
        os.system('tput reset')
        fourth = int(self.screen['columns'] / 4) - 8
        combined_list = list([self.maps[x].map_array for x in range(self.num_players)])
        for i in zip(*combined_list):
            for j, item in enumerate(i):
                for k in item[self.left_pointer[j]:self.right_pointer[j]]:
                    print(k, end='')
                print(config.LINE, end='')
            print()
            print('\r', end='')

        # for i in self.maps[x].map_array[:]:
        #     for j in i[self.left_pointer[x]:self.right_pointer[x]]:
        #         print(j, end='')
        #     print()
        #     print('\r', end='')
        # print('\r' + config.SCORE_TITLE + ": " + str(self.players[x].score),
        #       config.TIME + ': ' + str(self.players[x].time), config.LEVEL_I_TITLE,
        #       config.STONE + ' * ' + str(self.players[x].stones),
        #       config.LOVE + ' *' + str(self.players[x].get_lives()),
        #       sep=' ' * fourth)
        # print('\r' + ' ' * config.SPACES_BEFORE_TITLE, config.TITLE)


game = Game(2)
