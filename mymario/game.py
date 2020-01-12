import os
import platform
import sys
from random import randrange
from threading import Thread, Timer
from time import sleep
import atexit

import keyboard

import config
import level1_map
from controls import Controls
from motion import Player, Stones
from objects import Obj
from music import Music


msc = Music()
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
        self.gameplay_settings = self.configure_gameplay_settings()
        # os.system('tput civis')
        # print("the ratio is ", columns / nop)
        self.welcome_screen()
        for num_id in range(nop):
            self.maps.append(level1_map.Level1Map(num_id, self.screen['rows'],
                                                  int(self.screen['columns'] / nop - 1)))
            self.players.append(
                Player(self.maps[-1].initial_player_position, config.PLAYER, num_id, self.maps[-1]))
        self.controls = Controls()
        # self.maps[0].view_map()
        # self.print_screen()
        # exit(1)
        if ROOT:
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
        else:
            time_thread = Thread(target=self.decrease_time, args=(0,))
            time_thread.daemon = True
            time_thread.start()
            all_input_thread = Thread(target=self.game_input)
            all_input_thread.daemon = True
            all_input_thread.start()
        msc.play_music_for_action('Player at start')
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

    def configure_gameplay_settings(self):
        gameplay_settings = {}
        if config.WINDOWS:
            gameplay_settings = config.DEFAULT_SETTINGS['windows-10']
        if config.LINUX:
            if config.UBUNTU1604:
                gameplay_settings = config.DEFAULT_SETTINGS['ubuntu-1604']
            elif config.UBUNTU1804:
                gameplay_settings = config.DEFAULT_SETTINGS['ubuntu-1804']
        return gameplay_settings

    def welcome_screen(self):
        print('Hi!, Welcome to "My Mario" Game'.center(self.screen['columns']))
        print('\rControls:')
        print("\r'w' -> to move up")
        print("\r'a' -> to move left")
        print("\r'd -> to move right'")
        print("\r'e' -> to move up_right")
        print("\r'z' -> to move back_left")
        print("\r'f' -> to throw stones")
        print("\r'SPACE_BAR' -> at any instance of game to pause and to resume")
        print("\r'q' -> at any instance of game to quit")
        print('\rPress any key to continue.')
        sys.stdin.read(1)

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
            msc.play_music_for_action('Game over', change=True,
                                                              no_thread=True)
            config.pause.set()
            config.timeout.set()

    def get_input_for_player(self, player_id):
        while True:
            self.move_player(player_id)
            sleep(0.03)

    def game_input(self):
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
                msc.play_music_for_action('Game paused')
                if config.pause.is_set():
                    config.pause.clear()
                else:
                    config.pause.set()

            if not config.pause.is_set() and not config.timeout.is_set():
                for player_id in range(self.num_players):
                    if k == self.controls.player[player_id].BULLET:
                        self.launch_stones(player_id)
                        break
            player_id = 0
            if self.players[player_id].is_alive and not config.pause.is_set() and not config.timeout.is_set():
                if k == self.controls.player[player_id].UP_LEFT:
                    self.players[player_id].move_up_left()
                if k == self.controls.player[player_id].UP_RIGHT:
                    self.players[player_id].move_up_right()
                if k == self.controls.player[player_id].LEFT:
                    self.players[player_id].move_left()
                if k == self.controls.player[player_id].RIGHT:
                    self.players[player_id].move_right()
                if k == self.controls.player[player_id].UP:
                    self.players[player_id].move_up()
            if config.timeout.is_set():
                break
            if config.stop.is_set():
                break


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
        if not self.players[player_id].is_alive:
            return
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
        print("\033[?1049h\033[H")
        # Obj(self.screen['columns'], self.screen['rows'], 1, 3, ' ')

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
        if config.LINUX:
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
        if self.num_players == 1:
           self.maps[0].control_music(self.players[0].min_x)

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
        # os.system(config.CLEAR_COMMAND)
        print('\033[0;0f',end='')
        combined_list = list([self.maps[x].map_array for x in range(self.num_players)])
        skip = False
        if self.gameplay_settings['force_emoji']:
            for i in zip(*combined_list):
                for j, item in enumerate(i):
                    for k in item[self.maps[j].left_pointer:self.maps[j].right_pointer]:
                        if skip:
                            skip = False
                        else: print(k, end='')
                        if k in config.hard_emojis:
                            if not k == item[self.maps[j].right_pointer-1]:
                                skip = True
                    print(config.LINE, end='')
                print('\r')
        else:
            for i in zip(*combined_list):
                for j, item in enumerate(i):
                    for k in item[self.maps[j].left_pointer:self.maps[j].right_pointer]:
                       print(k,end='')
                    print(config.LINE, end='')
                print('\r')

        string_length = len('SCORE: ⌛: LEVEL I ⚽ *❤️* ')
        for x in range(self.num_players):
            total_length = string_length + len(
                str(self.players[x].score) + str(self.players[x].time) + str(
                    self.players[x].stones) + str(self.players[x].get_lives()))
            if config.UBUNTU1804:
                total_length += 2
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
            print("\033[?1049l")
            # os.system('clear')
            # os.system('tput reset')
            # os.system('reset')
        last_string = "Thanks for playing My Mario game."
        'Your score: " + str(c.PLAYER_OBJ[0].score)'
        print(last_string.center(self.screen['columns']))
        print("\rScores:")
        [print('\r  Player', player_num + 1, ":", self.players[player_num].score) for player_num in
         range(self.num_players)]
        print('\r',end='')
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

def exit_handler(stdin_fd, terminal_settings):
    if config.WINDOWS:
        return
    if config.LINUX:
        import termios
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, terminal_settings)
        os.system('killall -q aplay 2 >/dev/null')
        # print("\033[?1049l")


if __name__ == "__main__":
    settings_term = None
    stdin_fd = sys.stdin.fileno()
    if config.LINUX:
        import termios, tty
        settings_term = termios.tcgetattr(stdin_fd)
        tty.setraw(stdin_fd)

        os.system('tput civis')
    atexit.register(exit_handler, stdin_fd=stdin_fd, terminal_settings=settings_term)
    ROOT = True
    if len(sys.argv) > 1:
        if sys.argv[1] == "-n":
            ROOT = False
    # print("LINUX: ", LINUX)
    if ROOT:
        game = Game(4)
    else:
        game = Game(1)
