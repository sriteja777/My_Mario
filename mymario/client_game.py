import ast
import os
import platform
import sys
from random import randrange
from threading import Thread, Timer
from time import sleep, time
import atexit

import keyboard

import config
import level1_map
from controls import Controls
from motion import Player, Stones
from objects import Obj
from music import Music
from utils import to_camel_case, DaemonThread
from network.client import Client
import store

inc = 0


class Game:
    def __init__(self):
        self.client = Client()
        self.client.connect_to_server()
        server_config = self.client.receive()
        # rows, columns = self.get_terminal_dimensions()
        self.screen = server_config['screen']
        nop = server_config['nop']
        game_map = server_config['game_map']
        # exit(1)
        self.player_id = 1
        self.num_players = server_config['nop']
        mct = server_config["mct"] + self.client.time_diff
        sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=self.screen['rows'], cols=self.screen['columns']))
        # if not self.multi_player_support(nop):
        #     print("Sorry " + str(nop) + " is not supported at present screen aspect ratio.")
        #     return
        self.initialise_screen()
        self.players = []

        self.gameplay_settings = self.configure_gameplay_settings()
        while True:
            if time() >= mct:
                break
        self.map = self.get_map_class(game_map)(0, self.screen["rows"], self.screen['columns'], self.player_id)
        print("\rActual times")
        [print('\r', i["range"], i['time'] - self.client.time_diff) for i in store.enemy_times]
        # exit(1)
        move_pointer = False
        for player in range(self.num_players):
            if player == self.player_id:
                move_pointer, check_ends = True, True
            else:
                move_pointer,check_ends = False, False
            self.players.append(Player(self.map.initial_player_position[player], config.PLAYER, 0, self.map, move_pointer, check_ends))
        print(self.players[self.player_id].check_ends)
        print(self.players[0].check_ends)
        # exit(1)
        self.controls = Controls()

        inp_thread = DaemonThread(target=self.get_input_for_player, args=(self.player_id,))
        # time_thread = DaemonThread(target=self.decrease_time, args=(self,))
        network_thread = DaemonThread(target=self.receive_stats)
        game_control_thread = DaemonThread(target=self.get_input_for_control)
        self.map.map_array[3][10:16] = "Client"
        while True:
            try:
                if config.stop.is_set() or config.timeout.is_set():
                    break
                sleep(0.1)
                [self.make_updates(x) for x in range(self.num_players)]
                self.updates()

            except KeyboardInterrupt:
                break
        # self.exit()

    def move_a_player(self, player_id, command):
        eval("self.players[player_id].move_" + command + "()")

    def receive_stats(self):
        while True:
            data = self.client.receive()
            # print(str(data) * 10000)
            if data['object'] == "player":
                self.move_a_player(data['player_id'], data['command'])

    def make_updates(self, x):
        """
        Make updates and prints the map to the terminal
        :return:
        """
        global inc
        # for stone in self.players[x].stones_reference:
        #     temp = Thread(target=stone.move_stone)
        #     temp.daemon = True
        #     temp.start()
        #     if not stone.is_alive:
        #         self.players[x].stones_reference.remove(stone)
        # if self.num_players == 1:
           # self.maps[0].control_music(self.players[0].min_x)

        # rand_x = randrange(1, 100)
        # rand_x_2 = randrange(1, 150)
        # rand_x_3 = randrange(1, 75)
        # if inc % rand_x == 0:
        #     self.maps[x].clouds[0].move_cloud()
        # if inc % rand_x_2 == 0:
        #     self.maps[x].clouds[1].move_cloud()
        # if inc % rand_x_3 == 0:
        #     self.maps[x].clouds[2].move_cloud()
        # inc += 1

    def updates(self):
        os.system(config.CLEAR_COMMAND)
        # combined_list = list([self.maps[x].map_array for x in range(self.num_players)])
        skip = False
        if self.gameplay_settings['force_emoji']:
            for i in self.map.map_array:
                # for j, item in enumerate(i):
                for k in i[self.map.left_pointer:self.map.right_pointer]:
                    if skip:
                        skip = False
                    else: print(k, end='')
                    if k in config.hard_emojis:
                        # if not k == item[self.map.right_pointer-1]:
                        skip = True
                print('\r')
                # print(config.LINE, end='')
            print('\r',end='')
        else:
            pass
            # for i in zip(*combined_list):
            #     for j, item in enumerate(i):
            #         for k in item[self.maps[j].left_pointer:self.maps[j].right_pointer]:
            #            print(k,end='')
            #         print(config.LINE, end='')
            #     print('\r')

        # string_length = len('SCORE: ⌛: LEVEL I ⚽ *❤️* ')
        # for x in range(self.num_players):
        #     total_length = string_length + len(
        #         str(self.players[x].score) + str(self.players[x].time) + str(
        #             self.players[x].stones) + str(self.players[x].get_lives()))
        #     if config.UBUNTU1804:
        #         total_length += 2
        #     gap = int((self.maps[x].columns - total_length) / 4)
        #     print(config.SCORE_TITLE + ": " + str(self.players[x].score),
        #           config.TIME + ': ' + str(self.players[x].time), config.LEVEL_I_TITLE,
        #           config.STONE + ' * ' + str(self.players[x].stones),
        #           config.LOVE + ' *' + str(self.players[x].get_lives()), sep=' ' * gap,
        #           end=' ' * (self.maps[x].columns - total_length - 4 * gap + 2))

        print('\n\r', end='')
        # print(config.TITLE.center(self.screen['columns']+len(config.TITLE) - len('MY MARIO')))
        # Either this or below statement can be used.
        print('{: ^{num}}'.format(config.TITLE,
                                  num=self.screen['columns'] + len(config.TITLE) - len('MY MARIO')))


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
                        # self.launch_stones(player_id)
                        break
            if config.timeout.is_set():
                break
            if config.stop.is_set():
                break

    def move_player(self, player_id):
        if keyboard.is_pressed(self.controls.player[player_id].LEFT):
            self.client.send({"object": "player", "player_id": self.player_id, "command": "left"})
            self.players[player_id].move_left()
        if keyboard.is_pressed(self.controls.player[player_id].UP):
            self.client.send({"object": "player", "player_id": self.player_id, "command": "up"})
            self.players[player_id].move_up()
        if keyboard.is_pressed(self.controls.player[player_id].RIGHT):
            self.client.send({"object": "player", "player_id": self.player_id, "command": "right"})
            self.players[player_id].move_right()
        if keyboard.is_pressed(self.controls.player[player_id].UP_RIGHT):
            self.client.send({"object": "player", "player_id": self.player_id, "command": "up_right"})
            self.players[player_id].move_up_right()
        if keyboard.is_pressed(self.controls.player[player_id].UP_LEFT):
            self.client.send({"object": "player", "player_id": self.player_id, "command": "up_left"})
            self.players[player_id].move_up_left()

    def get_input_for_player(self, player_id):
        while True:
            self.move_player(player_id)
            sleep(0.03)

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
            config.pause.set()
            config.timeout.set()

    @staticmethod
    def get_map_class(game_map):
        map_class = None
        try:
            map_module = __import__(game_map)
            map_class = getattr(map_module, to_camel_case(game_map))
            # print(map_class)
        except (ModuleNotFoundError, AttributeError) as e:
            print(
                "Sorry given map not found, Strictly follow naming comventions for the map modules.")
            exit(1)
        return map_class

    @staticmethod
    def get_terminal_dimensions():
        if config.LINUX:
            rows, columns = os.popen('stty size', 'r').read().split()
            return int(rows) - 3, int(columns)
        else:
            rows, columns = 41, 168
            return rows, columns

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

    @staticmethod
    def initialise_screen():
        print("\033[?1049h\033[H")

    @staticmethod
    def configure_gameplay_settings():
        gameplay_settings = {}
        if config.WINDOWS:
            gameplay_settings = config.DEFAULT_SETTINGS['windows-10']
        if config.LINUX:
            if config.UBUNTU1604:
                gameplay_settings = config.DEFAULT_SETTINGS['ubuntu-1604']
            elif config.UBUNTU1804:
                gameplay_settings = config.DEFAULT_SETTINGS['ubuntu-1804']
        return gameplay_settings


def exit_handler(stdin_fd, terminal_settings):
    if config.WINDOWS:
        return
    if config.LINUX:
        import termios
        termios.tcsetattr(stdin_fd, termios.TCSADRAIN, terminal_settings)
        os.system('killall -q aplay 2 >/dev/null')
        os.system("tput cnorm")
        game.client.close()
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
    ROOT = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "-n":
            ROOT = False
    game = Game()
    # print("LINUX: ", LINUX)
    # if ROOT:
    #     game = Game(1)
    # else:
    #     game = Game(2)
