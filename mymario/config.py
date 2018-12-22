"""
Config file for the game
"""

import os
from threading import Event, main_thread
print(os.popen('stty size', 'r').read().split())
ROWS, COLUMNS = os.popen('stty size', 'r').read().split()
ROWS, COLUMNS = int(ROWS) - 3, int(COLUMNS)
MAP_LENGTH = 5 * COLUMNS
DIMENSIONAL_ARRAY = [[' ' for x in range(1, MAP_LENGTH + 1)] for y in range(1, ROWS + 1)]
OBJECT_ARRAY = [[0 for _ in range(1, MAP_LENGTH + 1)] for _ in range(1, ROWS + 1)]
# MAP_ARRAY = [[' ' for _ in range(1, 3*COLUMNS+1)] for _ in range(1, ROWS+1)]


# Define all the required colors
COLORS = {
    'Black': '\x1b[0;30m',
    'Blue': '\x1b[1;34m',
    'Green': '\x1b[0;32m',
    'Cyan': '\x1b[0;36m',
    'Red': '\x1b[1;31m',
    'Purple': '\x1b[0;35m',
    'Brown': '\x1b[0;33m',
    'Gray': '\x1b[0;37m',
    'Pink': '\x1b[38;5;200m',
    'Dark Gray': '\x1b[1;30m',
    'Light Blue': '\x1b[1;34m',
    'Light Green': '\x1b[1;32m',
    'Light Cyan': '\x1b[1;36m',
    'Light Red': '\x1b[1;31m',
    'Light Purple': '\x1b[1;35m',
    'Yellow': '\x1b[1;33m',
    'Light Grey': '\x1b[1;37m',
    'Bridge Color': '\x1b[48;5;130m',
    'Bullets Color': '\x1b[38;5;208m',
    'Extras Bridge': '\x1b[38;5;82m',
    'Water Color': '\x1b[48;5;39m',
    'Fish Color': '\x1b[38;5;130m',
    'Moving Bridges': '\x1b[48;5;94m'
}

# Define all the required global variables
END_COLOR = '\033[0m'
TITLE = COLORS['Blue'] + 'SUPER MARIO' + END_COLOR
SPACES_BEFORE_TITLE = int(COLUMNS / 2 - len(TITLE) / 2)
INITIAL_SCORE = 0
SCORE_TITLE = COLORS['Purple'] + "SCORE" + END_COLOR
TIME = COLORS['Green'] + "⌛" + END_COLOR
LEVEL_I_TITLE = COLORS['Pink'] + 'LEVEL I' + END_COLOR
COIN = COLORS['Yellow'] + '💰' + END_COLOR
ENEMY = COLORS['Red'] + '^' + END_COLOR
BRIDGE = COLORS['Bridge Color'] + '_' + END_COLOR
DOWN_WALL = COLORS['Brown'] + '░' + END_COLOR
UP_WALL = COLORS['Light Green'] + '▓' + END_COLOR
FLAG_POST = '|'
STONE = COLORS['Bullets Color'] + '⚽' + END_COLOR
WATER = COLORS['Water Color'] + '░' + END_COLOR
MOVING_BRIDGES = COLORS['Moving Bridges'] + '|' + END_COLOR
# PLAYER = '\033[1;34;' + '@'
PLAYER = COLORS['Cyan'] + '@' + END_COLOR
DEFAULT_LIVES = 5
DEFAULT_NO_OF_STONES = 3
DEFAULT_TIMEOUT = 200
LOVE = COLORS['Red'] + '❤️' + END_COLOR
EXTRAS_BRIDGE = COLORS['Extras Bridge'] + '░' + END_COLOR
FISH = COLORS['Fish Color'] + COLORS['Water Color'] + '🐠' + END_COLOR
THRONES = '┴'
MUSIC_FILES_PATH = './Media/'
TOP = int(4 + ROWS / 20)
BRIDGE_LIST = []
COINS_LIST = []
CLOUD_LIST = []
ENEMIES_LIST = []
HOLES_LIST = []  # Done
SUB_HOLES_LIST = []  # Done
STONES_LIST = []  # Done
POLE = []  # Done
PLAYER_OBJ = []  # Done
EXTRAS = []  # Done
LAKES = []  # Done
LIFE = []  # Done
FISHES = []  # Done
THRONES_LIST = []  # Done
MOVING_BRIDGES_OBJ = []  # Done
left_pointer = [0, ]  # Done
right_pointer = [COLUMNS, ]  # Done
stop = Event()
pause = Event()
level_finished = Event()
timeout = Event()
player_killed = Event()
CHECKPOINTS = []  # Done
CONTROL_MUSIC = []


def getch_unix():
    """
    Get the singe character typed on terminal on Unix-based systems
    :return: Single character typed during game
    """
    import sys
    import tty
    import termios
    file_desc = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_desc)
    try:
        tty.setraw(sys.stdin.fileno())
        char = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_desc, termios.TCSADRAIN, old_settings)
    return char


def _music(action):
    """
    Plays the given music filename
    :param action:
    :return:
    """
    if main_thread().is_alive():
        os.system('aplay -q ./Media/' + action + '.wav > /dev/null')
    # os.system('aplay ~/Music/super\ mario/40.wav')


def play_music_thread(action='start', no_thread=False, change=False):
    """
    Plays the given music
    :param action: Music file name to play
    :param no_thread: boolean whether to play music in parallel or not
    :param change: boolean whether to change the correct music or not
    :return:
    """
    if change:
        os.system('killall -q aplay 2> /dev/null')
    if not no_thread:
        from threading import Thread
        temp = Thread(target=_music, args=(action,))
        temp.daemon = True
        temp.start()
    else:
        _music(action)
    # if change:
    #     temp = Thread(target=_music, args=(action, ))
    #     temp.daemon = True
    #     temp.start()

