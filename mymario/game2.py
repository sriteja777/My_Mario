import os
import platform
from random import randrange
from threading import Thread, Timer
from time import sleep

import keyboard

import config
import level1_map
from controls import Controls
from motion import Player, Stones
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
        self.players = []
        self.maps = []
        print("the ratio is ", columns / nop)
        for num_id in range(nop):
            self.maps.append(level1_map.Level1Map(num_id, self.screen['rows'],
                                                  int(self.screen['columns'] / nop - 1)))
            self.players.append(
                Player(self.maps[-1].initial_player_position, config.PLAYER, num_id, self.maps[-1]))
        self.controls = Controls()
        # self.maps[0].view_map()
        # self.print_screen()
        # exit(1)
        for player_id in range(self.num_players):
            inp_thread = Thread(target=self.get_input_for_player, args=(player_id,))
            inp_thread.daemon = True
            inp_thread.start()
            time_thread = Thread(target=self.decrease_time, args=(player_id,))
            time_thread.daemon = True
            time_thread.start()
        control_input_thread = Thread(target=self.get_input_for_control)
        control_input_thread.daemon = True
        control_input_thread.start()
        while True:
            try:
                if config.stop.is_set() or config.timeout.is_set():
                    break
                sleep(0.1)
                [self.make_updates(x) for x in range(self.num_players)]
                self.updates()

            except KeyboardInterrupt:
                break
        self.exit()

    def decrease_time(self, player_id):
        """
        Decreases Game Timer by 1 recursively itself after 1 sec
        :return:
        """
        if self.players[player_id].time > 0:
            if not config.pause.is_set() and self.players[player_id].is_alive:
                self.players[player_id].time -= 1

            temp = Timer(1, self.decrease_time, args=[player_id, ])
            temp.daemon = True
            temp.start()
        else:
            if config.SOUND:
                config.CONTROL_MUSIC[0].play_music_for_action('Game over', change=True,
                                                              no_thread=True)
            config.pause.set()
            config.timeout.set()

    def get_input_for_player(self, player_id):
        pass
        if config.LINUX:
            import sys
            import tty
            import termios
            while True:
                file_desc = sys.stdin.fileno()
                old_settings = termios.tcgetattr(file_desc)
                try:
                    tty.setraw(sys.stdin.fileno())
                    sleep(0.03)
                    self.move_player(player_id)
                finally:
                    termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
        elif config.WINDOWS:
            while True:
                self.move_player(player_id)
                sleep(0.03)


    def get_input_for_control(self):
        if config.LINUX:
            getch = config.getch_unix
        elif config.WINDOWS:
            getch = config.getch_windows
        else:
            return
        while True:
            k = getch()
            if k == 'q':
                config.stop.set()
                break

            if k == ' ':
                # pause the game
                if config.SOUND:
                    config.CONTROL_MUSIC[0].play_music_for_action('Game paused')
                if config.pause.is_set():
                    config.pause.clear()
                else:
                    config.pause.set()

            if not config.pause.is_set() and not config.timeout.is_set():
                for player_id in range(self.num_players):
                    if k == self.controls.player[player_id].BULLET:
                        self.launch_stones(player_id)
                        break
            if config.timeout.is_set():
                break
            if config.stop.is_set():
                break

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
        # if keyboard.is_pressed(self.controls.player[player_id].BULLET):
        #     self.launch_stones(player_id)

    def launch_stones(self, player_id):
        if self.players[player_id].is_alive:
            if self.players[player_id].stones > 0:
                self.players[player_id].stones_reference.append(
                    Stones(self.players[player_id].max_x + 1, self.players[player_id].min_y,
                           self.players[player_id].max_x + 1, self.players[player_id].min_y,
                           config.STONE, self.maps[player_id],
                           self.players[player_id].update_score))
                self.players[player_id].stones -= 1

    def multi_player_support(self, num_of_players):
        """
        Returns whether num_of_players multi playing is supported or not.
        Calculated by the ratio columns/num_of_players. By experimental observations, if the ratio
        is greater than 40, then multi playing is supported else not. (But there are some exceptions
        too, this formula doesn't work well for high terminal sizes.)
        :param num_of_players: Number of players
        :return: True is supported else False
        """
        if self.screen['columns'] / num_of_players > 40:
            return True
        else:
            return False

    def initialise_screen(self):
        Obj(self.screen['columns'], self.screen['rows'], 1, 3, ' ')

    def print_screen(self):
        lp = 0
        rp = int(self.screen['columns'] / self.num_players - 1)
        combined_list = list([self.maps[x].map_array for x in range(self.num_players)])
        for i in zip(*combined_list):
            for j in i:
                for k in j[lp:rp]:
                    print(k, end='')
                print(config.LINE, end='')
            print()
            print('\r', end='')

    @staticmethod
    def get_terminal_dimensions():
        if platform.system() != "Windows":
            rows, columns = os.popen('stty size', 'r').read().split()
            return int(rows) - 3, int(columns)
        else:
            rows, columns = 41, 168
            return rows, columns

    def make_updates(self, x):
        """
        Make updates and prints the map to the terminal
        :return:
        """
        global inc
        for stone in self.players[x].stones_reference:
            temp = Thread(target=stone.move_stone)
            temp.daemon = True
            temp.start()
            if not stone.is_alive:
                self.players[x].stones_reference.remove(stone)
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
        os.system(config.CLEAR_COMMAND)
        combined_list = list([self.maps[x].map_array for x in range(self.num_players)])
        for i in zip(*combined_list):
            for j, item in enumerate(i):
                for k in item[self.maps[j].left_pointer:self.maps[j].right_pointer]:
                    print(k, end='')
                print(config.LINE, end='')
            print()
            print('\r', end='')

        string_length = len('SCORE: ⌛: LEVEL I ⚽ *❤️* ')
        for x in range(self.num_players):
            total_length = string_length + len(
                str(self.players[x].score) + str(self.players[x].time) + str(
                    self.players[x].stones) + str(self.players[x].get_lives()))
            gap = int((self.maps[x].columns - total_length) / 4)
            print(config.SCORE_TITLE + ": " + str(self.players[x].score),
                  config.TIME + ': ' + str(self.players[x].time), config.LEVEL_I_TITLE,
                  config.STONE + ' * ' + str(self.players[x].stones),
                  config.LOVE + ' *' + str(self.players[x].get_lives()), sep=' ' * gap,
                  end=' ' * (self.maps[x].columns - total_length - 4 * gap + 2))

        print('\n\r', end='')
        # print(config.TITLE.center(self.screen['columns']+len(config.TITLE) - len('MY MARIO')))
        # Either this or below statement can be used.
        print('{: ^{num}}'.format(config.TITLE,
                                  num=self.screen['columns'] + len(config.TITLE) - len('MY MARIO')))

    def exit(self):
        """
        Exit the game
        :return:
        """
        if config.LINUX:
            os.system("tput cnorm")
            os.system("tput cnorm")
            os.system('killall -q aplay 2 >/dev/null')
            os.system('reset')
        last_string = "Thanks for playing My Mario game."
        'Your score: " + str(c.PLAYER_OBJ[0].score)'
        print(last_string.center(self.screen['columns']))
        print("Scores:")
        [print('Player', player_num + 1, ":", self.players[player_num].score) for player_num in
         range(self.num_players)]
        if config.LINUX:
            os.system('killall -q aplay 2 >/dev/null')
        exit(0)


# import os, subprocess


# def prompt_sudo():
#     ret = 0
#     if os.geteuid() != 0:
#         msg = "[sudo] password for %u:"
#         ret = subprocess.check_call("sudo -v -p '%s'" % msg, shell=True)
#     return ret
#
#
# while prompt_sudo() != 0:
#     print("You enter incorrect password please try again")
game = Game(1)
