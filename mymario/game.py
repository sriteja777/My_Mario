"""
Main file for running the game
"""
import os
from random import randrange
from threading import Thread, Timer
from time import sleep

import config as c
from irregular import IrregularObjects, print_cloud
from motion import Player, Stones, Enemies, MovingBridges
from music import Music
from objects import Obj, Extras

inc = 0


# changed_1 = False
# changed_2 = False
# changed_3 = False


def decrease_time():
    """
    Decreases Game Timer by 1 recursively itself after 1 sec
    :return:
    """
    if c.PLAYER_OBJ[0].time > 0:
        if not c.pause.is_set() and c.PLAYER_OBJ[0].is_alive:
            c.PLAYER_OBJ[0].time -= 1

        temp = Timer(1, decrease_time)
        temp.daemon = True
        temp.start()
    else:
        c.CONTROL_MUSIC[0].play_music_for_action('Game over', change=True, no_thread=True)
        c.pause.set()
        c.timeout.set()


def get_extra():
    """
    Returns any random extra point when PLAYER_OBJ touches extra bridges
    :return: Returns the string of extra point
    """
    num = randrange(0, 3)
    if num == 0:
        return c.TIME
    if num == 1:
        return c.LOVE
    # x = 2
    return c.STONE


def create_level1_map():
    """
    Initialises level 1 map of game
    :return:
    """
    # Create the ground for the PLAYER_OBJ
    down_wall = Obj(c.MAP_LENGTH, c.ROWS, 1, int((9 * c.ROWS) / 10), c.DOWN_WALL)
    up_wall = Obj(c.MAP_LENGTH, down_wall.min_y - 1, 1, down_wall.min_y - 1, c.UP_WALL)

    # Create bridges(some at random place and some at predefined place)
    c.BRIDGE_LIST.append(Obj(20, up_wall.min_y - 5, 14, up_wall.min_y - 7, c.BRIDGE))
    c.BRIDGE_LIST.append(Obj(40, up_wall.min_y - 5, 25, up_wall.min_y - 7, c.BRIDGE))
    c.BRIDGE_LIST.append(
        Obj(c.COLUMNS - 4, up_wall.min_y - 1, c.COLUMNS - 10, up_wall.min_y - 7, c.BRIDGE))
    rand_x = randrange(c.COLUMNS + 5, int(4 * c.COLUMNS / 3) - 5)
    c.BRIDGE_LIST.append(
        Obj(5 + rand_x, up_wall.min_y - 5, rand_x - 5, up_wall.min_y - 8, c.BRIDGE))
    rand_x = randrange(int(5 * c.COLUMNS / 3) + 1, 2 * c.COLUMNS - 2)
    c.BRIDGE_LIST.append(
        Obj(rand_x + 1, up_wall.min_y - 6, rand_x - 1, up_wall.min_y - 8, c.BRIDGE))
    rand_x = randrange(2 * c.COLUMNS + 6, int((7 * c.COLUMNS) / 3) - 6)
    cross_bridge_list = [[' ' for _ in range(0, 15)] for _ in range(0, 15)]
    for x_pos in range(0, 15):
        for y_pos in range(15 - x_pos, 15):
            cross_bridge_list[x_pos][y_pos] = c.BRIDGE
    c.BRIDGE_LIST.append(IrregularObjects(
        {'max_x': rand_x + 6, 'max_y': up_wall.min_y - 1, 'min_x': rand_x - 6,
         'min_y': up_wall.min_y - 14}, cross_bridge_list))

    # Create EXTRAS
    mid = int((c.BRIDGE_LIST[1].min_x + c.BRIDGE_LIST[1].max_x) / 2)
    c.EXTRAS.append(
        Extras(mid + 1, c.BRIDGE_LIST[1].max_y, mid - 1, c.BRIDGE_LIST[1].min_y, c.EXTRAS_BRIDGE,
               get_extra()))
    mid = int((c.BRIDGE_LIST[3].min_x + c.BRIDGE_LIST[3].max_x) / 2)
    c.EXTRAS.append(
        Extras(mid + 1, c.BRIDGE_LIST[3].max_y, mid - 1, c.BRIDGE_LIST[3].min_y, c.EXTRAS_BRIDGE,
               get_extra()))

    # Create holes
    rand_x = randrange(int(c.COLUMNS / 3), int((2 * c.COLUMNS) / 3))
    c.HOLES_LIST.append(Obj(rand_x + 5, down_wall.max_y - 2, rand_x, up_wall.min_y, ' '))
    c.SUB_HOLES_LIST.append(Obj(c.HOLES_LIST[0].max_x + 10, c.HOLES_LIST[0].max_y,
                                c.HOLES_LIST[0].min_x, up_wall.min_y + 2, ' '))
    rand_x = randrange(int((4 * c.COLUMNS) / 3) + 4, int(5 * c.COLUMNS / 3) - 4)
    c.HOLES_LIST.append(Obj(rand_x + 4, c.ROWS, rand_x - 4, up_wall.min_y, ' '))
    c.HOLES_LIST.append(
        Obj(c.BRIDGE_LIST[5].max_x + 24, c.ROWS, c.BRIDGE_LIST[5].max_x + 1, up_wall.min_y, ' '))

    # Create Coins
    mid = int((c.BRIDGE_LIST[0].min_x + c.BRIDGE_LIST[0].max_x) / 2)
    c.COINS_LIST.append(
        Obj(mid, c.BRIDGE_LIST[0].min_y - 1, mid, c.BRIDGE_LIST[0].min_y - 1, c.COIN))
    mid = int((c.BRIDGE_LIST[1].min_x + c.BRIDGE_LIST[1].max_x) / 2)
    for x_pos, y_pos in zip(range(mid - 4, mid + 2, 2),
                            range(c.BRIDGE_LIST[1].min_y - 1, c.BRIDGE_LIST[1].min_y - 4, -1)):
        c.COINS_LIST.append(Obj(x_pos, y_pos, x_pos, y_pos, c.COIN))
    for x_pos, y_pos in zip(range(mid + 2, mid + 8, 2),
                            range(c.BRIDGE_LIST[1].min_y - 2, c.BRIDGE_LIST[1].min_y, 1)):
        c.COINS_LIST.append(Obj(x_pos, y_pos, x_pos, y_pos, c.COIN))
    print(c.SUB_HOLES_LIST[0].max_x, c.SUB_HOLES_LIST[0].max_y)

    c.COINS_LIST.append(Obj(c.SUB_HOLES_LIST[0].max_x, c.SUB_HOLES_LIST[0].max_y,
                            c.SUB_HOLES_LIST[0].max_x, c.SUB_HOLES_LIST[0].max_y, c.TIME))
    for x_pos in range(c.HOLES_LIST[0].max_x + 5, c.BRIDGE_LIST[2].min_x - 5, 3):
        c.COINS_LIST.append(Obj(x_pos, up_wall.min_y - 1, x_pos, up_wall.min_y - 1, c.COIN))

    # Create lake and FISHES
    min_x = int(8 * c.COLUMNS / 3)
    max_x = int(11 * c.COLUMNS / 3)
    c.LAKES.append(Obj(max_x, down_wall.max_y - 1, min_x, up_wall.max_y, c.WATER))
    rand_x = randrange(c.LAKES[0].min_x + 2, c.LAKES[0].max_x - 2)
    rand_y = c.LAKES[0].min_y + randrange(1, 4)
    c.FISHES.append(Obj(rand_x, rand_y, rand_x, rand_y, c.FISH))
    rand_x = randrange(c.LAKES[0].min_x + 2, c.LAKES[0].max_x - 2)
    rand_y = c.LAKES[0].min_y + randrange(1, 4)
    c.FISHES.append(Obj(rand_x, rand_y, rand_x, rand_y, c.FISH))

    # Generate Clouds
    cloud = print_cloud()
    rand_x = randrange(1, c.COLUMNS)
    rand_x_2 = randrange(c.COLUMNS, 2 * c.COLUMNS)
    rand_x_3 = randrange(2 * c.COLUMNS, 3 * c.COLUMNS)
    c.CLOUD_LIST.append(IrregularObjects(
        {'max_x': len(cloud[0]) + rand_x, 'max_y': 5 + len(cloud), 'min_x': rand_x, 'min_y': 1},
        cloud))
    c.CLOUD_LIST.append(IrregularObjects(
        {'max_x': len(cloud[0]) + rand_x_2, 'max_y': 4 + len(cloud), 'min_x': rand_x_2, 'min_y': 2},
        cloud))
    c.CLOUD_LIST.append(IrregularObjects(
        {'max_x': len(cloud[0]) + rand_x_3, 'max_y': 6 + len(cloud), 'min_x': rand_x_3, 'min_y': 1},
        cloud))

    # Create Enemies
    c.ENEMIES_LIST.append(Enemies(c.SUB_HOLES_LIST[0].max_x - 2, c.SUB_HOLES_LIST[0].max_y,
                                  c.SUB_HOLES_LIST[0].max_x - 3,
                                  c.SUB_HOLES_LIST[0].max_y - 1, c.ENEMY, c.SUB_HOLES_LIST[0].min_x,
                                  c.SUB_HOLES_LIST[0].max_x - 2))
    c.ENEMIES_LIST.append(
        Enemies(c.HOLES_LIST[1].min_x - 1, up_wall.min_y - 1, c.HOLES_LIST[1].min_x - 2,
                up_wall.min_y - 2,
                c.ENEMY, c.BRIDGE_LIST[2].max_x + 1, c.HOLES_LIST[1].min_x - 1))
    c.ENEMIES_LIST.append(
        Enemies(c.BRIDGE_LIST[3].max_x, c.BRIDGE_LIST[3].min_y - 1, c.BRIDGE_LIST[3].max_x - 1,
                c.BRIDGE_LIST[3].min_y - 2, c.ENEMY, c.BRIDGE_LIST[3].min_x,
                c.BRIDGE_LIST[3].max_x))

    # Create enemies and bridges on lake
    mid = int((c.LAKES[0].min_x + c.LAKES[0].max_x) / 2)
    print(c.LAKES[0].min_y, c.LAKES[0].max_y)
    print('x_pos -> ', c.LAKES[0].min_x + 5, mid, 10)
    print('y_pos-> ', c.LAKES[0].min_y - 5, c.TOP - 3, int(c.ROWS / 10))
    # sleep(3)
    min_y = int(c.TOP + c.ROWS / 10)
    for x_pos, y_pos in zip(range(c.LAKES[0].min_x + 5, mid, 10),
                            range(c.LAKES[0].min_y - 5, min_y, -int(c.ROWS / 10))):
        c.BRIDGE_LIST.append(Obj(x_pos + 3, y_pos, x_pos - 3, y_pos - 1, c.BRIDGE))
        rand_x = randrange(x_pos - 3, x_pos + 3)
        c.ENEMIES_LIST.append(
            Enemies(rand_x + 1, y_pos - 2, rand_x, y_pos - 3, c.ENEMY, x_pos - 3, x_pos + 3))
    store = c.BRIDGE_LIST[-1]
    c.ENEMIES_LIST[-1].kill()
    c.ENEMIES_LIST.append(Enemies(store.max_x, store.min_y - 1, store.max_x - 1,
                                  store.min_y - 2, c.ENEMY, store.max_x - 1, store.max_x))

    for x_pos, y_pos in zip(range(c.LAKES[0].max_x - 5, mid, -10),
                            range(c.LAKES[0].min_y - 5, min_y, -int(c.ROWS / 10))):
        c.BRIDGE_LIST.append(Obj(x_pos + 3, y_pos, x_pos - 3, y_pos - 1, c.BRIDGE))
        rand_x = randrange(x_pos - 3, x_pos + 3)
        c.ENEMIES_LIST.append(
            Enemies(rand_x + 1, y_pos - 2, rand_x, y_pos - 3, c.ENEMY, x_pos - 3, x_pos + 3))
    store_2 = c.BRIDGE_LIST[-1]
    c.BRIDGE_LIST.append(Obj(store_2.min_x, store.max_y, store.max_x, store.min_y, c.BRIDGE))
    c.ENEMIES_LIST[-1].kill()
    c.ENEMIES_LIST.append(Enemies(store_2.min_x + 1, store_2.min_y - 1, store_2.min_x,
                                  store_2.min_y - 2, c.ENEMY, store_2.min_x, store_2.min_x + 1))
    mid = int((store.max_x + store_2.min_x) / 2)
    c.LIFE.append(Obj(mid, c.TOP, mid, c.TOP, c.LOVE))

    # Create moving bridges
    min_x = int((11 * c.COLUMNS) / 3) + 7
    length = 15
    max_x = int((9 * c.COLUMNS) / 2)

    # Create Knifes
    c.THRONES_LIST.append(Obj(max_x, up_wall.max_y + 1, min_x, up_wall.max_y, c.THRONES))

    min_y = c.TOP + 5
    max_y = c.LAKES[0].min_y - 5
    for x_pos in range(min_x, max_x, 25):
        rand_y = randrange(min_y, max_y + 1)
        c.MOVING_BRIDGES_OBJ.append(
            MovingBridges(x_pos + length, rand_y, x_pos, rand_y,
                          c.MOVING_BRIDGES, c.TOP + 5, c.LAKES[0].min_y - 5))

    # MOVING_BRIDGES_OBJ.append(MovingBridges(LAKES[0]))

    # Create the final POLE
    c.POLE.append(
        Obj(c.MAP_LENGTH - 5, up_wall.min_y - 1, c.MAP_LENGTH - 5, up_wall.min_y - 15, '|'))

    # Declare and start music
    c.CONTROL_MUSIC.append(Music())
    return up_wall, down_wall


def make_updates():
    """
    Make updates and prints the map to the terminal
    :return:
    """
    global inc

    for stone in c.STONES_LIST:
        temp = Thread(target=stone.move_stone)
        temp.daemon = True
        temp.start()
        if not stone.is_alive:
            c.STONES_LIST.remove(stone)
    if not c.CONTROL_MUSIC[0].player_crossed_start and \
            c.PLAYER_OBJ[0].min_x > c.HOLES_LIST[2].max_x:
        c.CONTROL_MUSIC[0].player_crossed_start = True
        c.CONTROL_MUSIC[0].play_music_for_action('Player at lake', change=True)
    if not c.CONTROL_MUSIC[0].player_crossed_lake and c.PLAYER_OBJ[0].min_x > c.LAKES[0].max_x:
        c.CONTROL_MUSIC[0].player_crossed_lake = True
        c.CONTROL_MUSIC[0].play_music_for_action('Player at thrones', change=True)
    if not c.CONTROL_MUSIC[0].player_crossed_thrones and \
            c.PLAYER_OBJ[0].min_x > c.THRONES_LIST[0].max_x:
        c.CONTROL_MUSIC[0].player_crossed_thrones = True
        c.CONTROL_MUSIC[0].play_music_for_action('Player at end', change=True)

    rand_x = randrange(1, 100)
    rand_x_2 = randrange(1, 150)
    rand_x_3 = randrange(1, 75)
    if inc % rand_x == 0:
        c.CLOUD_LIST[0].move_cloud()
    if inc % rand_x_2 == 0:
        c.CLOUD_LIST[1].move_cloud()
    if inc % rand_x_3 == 0:
        c.CLOUD_LIST[2].move_cloud()
    inc += 1
    os.system('tput reset')
    fourth = int(c.COLUMNS / 4) - 8

    for i in c.DIMENSIONAL_ARRAY[:]:
        for j in i[c.left_pointer[0]:c.right_pointer[0]]:
            print(j, end='')
        print()
        print('\r', end='')
    print('\r' + c.SCORE_TITLE + ": " + str(c.PLAYER_OBJ[0].score),
          c.TIME + ': ' + str(c.PLAYER_OBJ[0].time), c.LEVEL_I_TITLE,
          c.STONE + ' * ' + str(c.PLAYER_OBJ[0].stones),
          c.LOVE + ' *' + str(c.PLAYER_OBJ[0].get_lives()),
          sep=' ' * fourth)
    print('\r' + ' ' * c.SPACES_BEFORE_TITLE, c.TITLE)


def launch_stones():
    """
    Launch Stones by the PLAYER_OBJ
    :return:
    """
    if c.PLAYER_OBJ[0].is_alive:
        if c.PLAYER_OBJ[0].stones > 0:
            c.STONES_LIST.append(Stones(c.PLAYER_OBJ[0].max_x + 1, c.PLAYER_OBJ[0].min_y,
                                        c.PLAYER_OBJ[0].max_x + 1, c.PLAYER_OBJ[0].min_y, c.STONE))
            c.PLAYER_OBJ[0].stones -= 1


def get_input():
    """
    Get input from the user and perform corresponding actions in the game
    :return:
    """
    getch = c.getch_unix
    while True:
        k = getch()
        if k == 'q':
            c.stop.set()
            break

        if k == ' ':
            # pause the game
            c.CONTROL_MUSIC[0].play_music_for_action('Game paused')
            if c.pause.is_set():
                c.pause.clear()
            else:
                c.pause.set()

        if c.PLAYER_OBJ[0].is_alive and not c.pause.is_set() and not c.timeout.is_set():
            if k == 'a':
                c.PLAYER_OBJ[0].move_left()
            elif k == 'd':
                c.PLAYER_OBJ[0].move_right()
            elif k == 'w':
                c.PLAYER_OBJ[0].move_up()
            elif k == 'e':
                c.PLAYER_OBJ[0].move_up_right()
            elif k == 'z':
                c.PLAYER_OBJ[0].move_up_left()
            elif k == 'f':
                launch_stones()
        if c.timeout.is_set():
            break
        if c.stop.is_set():
            break


def exit_game():
    """
    Exit the game
    :return:
    """

    os.system("tput cnorm")
    os.system('killall -q aplay 2 >/dev/null')
    os.system('reset')
    last_string = "Thanks for playing my mario game. Your score: " + str(c.PLAYER_OBJ[0].score)
    print(last_string.center(c.COLUMNS))
    os.system('killall -q aplay 2 >/dev/null')
    exit(0)


# Initial Interactive
def start_screen():
    """
    Prints the help screen about the game
    :return:
    """
    try:
        os.system('clear')
        os.system('tput civis')
        print('Hi!, Welcome to "My Mario" Game'.center(c.COLUMNS))
        print('Controls:')
        print("'w' -> to move up")
        print("'a' -> to move left")
        print("'d -> to move right'")
        print("'e' -> to move up_right")
        print("'z' -> to move back_left")
        print("'f' -> to throw stones")
        print("'SPACE_BAR' -> at any instance of game to pause and to resume")
        print("'q' -> at any instance of game to quit")
        input('Press any key to continue.')
    except KeyboardInterrupt:
        os.system('tput cnorm')
        raise SystemExit(1)


def run():
    """
    Starts the game
    :return:
    """
    start_screen()
    # Initiate the screen
    Obj(c.COLUMNS, c.ROWS, 1, 3, ' ')
    up_wall, _ = create_level1_map()

    c.PLAYER_OBJ.append(
        Player({'max_x': 4, 'max_y': up_wall.min_y - 1, 'min_x': 3, 'min_y': up_wall.min_y - 2},
               c.PLAYER)
    )

    # Create CHECKPOINTS
    c.CHECKPOINTS.append((c.PLAYER_OBJ[0].min_x, c.PLAYER_OBJ[0].max_y))
    c.CHECKPOINTS.append((c.COLUMNS, up_wall.min_y - 1))
    c.CHECKPOINTS.append((c.HOLES_LIST[1].max_x + 4, up_wall.min_y - 1))
    c.CHECKPOINTS.append((c.HOLES_LIST[2].max_x + 4, up_wall.min_y - 1))
    c.CHECKPOINTS.append((c.LAKES[0].max_x + 1, up_wall.min_y - 1))
    c.CONTROL_MUSIC[0].play_music_for_action('Player at start')

    make_updates()
    inp_thread = Thread(target=get_input)
    inp_thread.daemon = True
    inp_thread.start()
    time_thread = Thread(target=decrease_time)
    time_thread.daemon = True
    time_thread.start()

    while True:
        try:
            if c.stop.is_set() or c.timeout.is_set():
                break
            sleep(0.1)
            make_updates()

        except KeyboardInterrupt:
            break

    exit_game()


if __name__ == '__main__':
    run()
