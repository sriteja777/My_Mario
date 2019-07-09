import os
from random import randrange
from threading import Thread
from time import sleep

import keyboard

import level1_map
import config
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
        # self.maps[0].view_map()
        self.print_screen()
        # inp_thread = Thread(target=self.temp)
        # inp_thread.daemon = True
        # inp_thread.start()
        inp = Thread(target=self.t1)
        inp.daemon= True
        inp2 = Thread(target=self.t2)
        inp2.daemon = True
        inp.start()
        inp2.start()
        while True:
            try:
                if config.stop.is_set() or config.timeout.is_set():
                    break
                sleep(0.1)
                [ self.make_updates(x) for x in range(self.num_players) ]
                self.updates()

            except KeyboardInterrupt:
                break

    def t1(self):
        while True:
            self.get_t1()

    def t2(self):
        while True:
            self.get_t2()

    def get_t1(self):
        import sys
        import tty
        import termios
        file_desc = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_desc)
        try:
            tty.setraw(sys.stdin.fileno())
            sleep(0.07)
            self.action_t1()
        finally:
            termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)

    def get_t2(self):
        import sys
        import tty
        import termios
        file_desc = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_desc)
        try:
            tty.setraw(sys.stdin.fileno())
            sleep(0.07)
            self.action_t2()
        finally:
            termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)

    def action_t1(self):
        if keyboard.is_pressed('a'):
            self.players[0].move_left()
        if keyboard.is_pressed('w'):
            self.players[0].move_up()
        if keyboard.is_pressed('d'):
            self.players[0].move_right()
        if keyboard.is_pressed('e'):
            self.players[0].move_up_right()
        if keyboard.is_pressed('z'):
            self.players[0].move_up_left()

    def action_t2(self):
        if keyboard.is_pressed('j'):
            self.players[1].move_left()
        if keyboard.is_pressed('i'):
            self.players[1].move_up()
        if keyboard.is_pressed('l'):
            self.players[1].move_right()
        if keyboard.is_pressed('o'):
            self.players[1].move_up_right()
        if keyboard.is_pressed('m'):
            self.players[1].move_up_left()



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

    def get_input(self):
        """
        Get input from the user and perform corresponding actions in the game
        :return:
        """
        getch = config.getch_unix
        while True:
            k = getch()
            if k == 'q':
                config.stop.set()
                break

            # if k == ' ':
            #     # pause the game
            #     c.CONTROL_MUSIC[0].play_music_for_action('Game paused')
            #     if c.pause.is_set():
            #         c.pause.clear()
            #     else:
            #         c.pause.set()

            if self.players[0].is_alive and not config.pause.is_set() and not config.timeout.is_set():
                if k == 'a':
                    self.players[0].move_left()
                elif k == 'd':
                    self.players[0].move_right()
                elif k == 'w':
                    self.players[0].move_up()

                elif k == 'e':
                    self.players[0].move_up_right()
                elif k == 'z':
                    self.players[0].move_up_left()
                elif k == 'f':
                    # launch_stones()
                    pass
                if k == 'j':
                    self.players[1].move_left()
                elif k == 'l':
                    self.players[1].move_right()
                elif k == 'i':
                    self.players[1].move_up()

                elif k == 'o':
                    self.players[1].move_up_right()
                elif k == 'm':
                    self.players[1].move_up_left()
            if config.timeout.is_set():
                break
            if config.stop.is_set():
                break


    def get_multiplayer_input(self):
        import sys
        import tty
        import termios
        file_desc = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_desc)
        try:
            tty.setraw(sys.stdin.fileno())
            char1 = None
            char2 = None
            # sys.stdin.read(1)
            sleep(0.07)
            self.action()
            # if keyboard.is_pressed('a'):
            #     char1 = 'a'
            #
            # elif keyboard.is_pressed('s'):
            #     char2 = 's'
            # if keyboard.is_pressed('q'):
            #     char1 = 'q'
        finally:
            termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
        return char1, char2

    def action(self):
        if keyboard.is_pressed('a'):
            self.players[0].move_left()
        if keyboard.is_pressed('w'):
            self.players[0].move_up()
        if keyboard.is_pressed('d'):
            self.players[0].move_right()
        if keyboard.is_pressed('e'):
            self.players[0].move_up_right()
        if keyboard.is_pressed('z'):
            self.players[0].move_up_left()
        if keyboard.is_pressed('j'):
            self.players[1].move_left()
        if keyboard.is_pressed('i'):
            self.players[1].move_up()
        if keyboard.is_pressed('l'):
            self.players[1].move_right()
        if keyboard.is_pressed('o'):
            self.players[1].move_up_right()
        if keyboard.is_pressed('m'):
            self.players[1].move_up_left()

    def temp(self):
        while True:
            # sleep(0.1)
            self.get_multiplayer_input()
            # self.action()


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
