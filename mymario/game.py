"""
Main file for running the game
"""
import os
from random import randrange
from threading import Thread, Timer
from time import sleep

import config as c
from irregular import IrregularObjects, print_cloud
from motion import Players, Stones, Enemies, MovingBridges
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
    if c.player[0].time > 0:
        if not c.pause.is_set():
            c.player[0].time -= 1

        temp = Timer(1, decrease_time)
        temp.daemon = True
        temp.start()
    else:
        c.control_music[0].play_music_for_action('Game over', change=True, no_thread=True)
        c.pause.set()
        c.timeout.set()


def get_extra():
    """
    Returns any random extra point when player touches extra bridges
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
    # Create the ground for the player
    down_wall = Obj(c.MAP_LENGTH, c.ROWS, 1, int((9 * c.ROWS) / 10), c.DOWN_WALL)
    up_wall = Obj(c.MAP_LENGTH, down_wall.min_y - 1, 1, down_wall.min_y - 1, c.UP_WALL)

    # Create bridges(some at random place and some at predefined place)
    c.bridge_list.append(Obj(20, up_wall.min_y - 5, 14, up_wall.min_y - 7, c.BRIDGE))
    c.bridge_list.append(Obj(40, up_wall.min_y - 5, 25, up_wall.min_y - 7, c.BRIDGE))
    c.bridge_list.append(
        Obj(c.COLUMNS - 4, up_wall.min_y - 1, c.COLUMNS - 10, up_wall.min_y - 7, c.BRIDGE))
    rand_x = randrange(c.COLUMNS + 5, int(4 * c.COLUMNS / 3) - 5)
    c.bridge_list.append(
        Obj(5 + rand_x, up_wall.min_y - 5, rand_x - 5, up_wall.min_y - 8, c.BRIDGE))
    rand_x = randrange(int(5 * c.COLUMNS / 3) + 1, 2 * c.COLUMNS - 2)
    c.bridge_list.append(
        Obj(rand_x + 1, up_wall.min_y - 6, rand_x - 1, up_wall.min_y - 8, c.BRIDGE))
    rand_x = randrange(2 * c.COLUMNS + 6, int((7 * c.COLUMNS) / 3) - 6)
    cross_bridge_list = [[' ' for _ in range(0, 15)] for _ in range(0, 15)]
    for x_pos in range(0, 15):
        for y_pos in range(15 - x_pos, 15):
            cross_bridge_list[x_pos][y_pos] = c.BRIDGE
    c.bridge_list.append(IrregularObjects(rand_x + 6, up_wall.min_y - 1, rand_x - 6,
                                          up_wall.min_y - 14, cross_bridge_list))

    # Create extras
    mid = int((c.bridge_list[1].min_x + c.bridge_list[1].max_x) / 2)
    c.extras.append(
        Extras(mid + 1, c.bridge_list[1].max_y, mid - 1, c.bridge_list[1].min_y, c.EXTRAS_BRIDGE,
               get_extra()))
    mid = int((c.bridge_list[3].min_x + c.bridge_list[3].max_x) / 2)
    c.extras.append(
        Extras(mid + 1, c.bridge_list[3].max_y, mid - 1, c.bridge_list[3].min_y, c.EXTRAS_BRIDGE,
               get_extra()))

    # Create holes
    rand_x = randrange(int(c.COLUMNS / 3), int((2 * c.COLUMNS) / 3))
    print(down_wall.max_y - 2)
    print(len(c.DIMENSIONAL_ARRAY))
    c.holes_list.append(Obj(rand_x + 5, down_wall.max_y - 2, rand_x, up_wall.min_y, ' '))
    c.sub_holes_list.append(Obj(c.holes_list[0].max_x + 10, c.holes_list[0].max_y,
                                c.holes_list[0].min_x, up_wall.min_y + 2, ' '))
    rand_x = randrange(int((4 * c.COLUMNS) / 3) + 4, int(5 * c.COLUMNS / 3) - 4)
    c.holes_list.append(Obj(rand_x + 4, c.ROWS, rand_x - 4, up_wall.min_y, ' '))
    c.holes_list.append(
        Obj(c.bridge_list[5].max_x + 24, c.ROWS, c.bridge_list[5].max_x + 1, up_wall.min_y, ' '))

    # Create Coins
    mid = int((c.bridge_list[0].min_x + c.bridge_list[0].max_x) / 2)
    c.coins_list.append(
        Obj(mid, c.bridge_list[0].min_y - 1, mid, c.bridge_list[0].min_y - 1, c.COIN))
    mid = int((c.bridge_list[1].min_x + c.bridge_list[1].max_x) / 2)
    for x_pos, y_pos in zip(range(mid - 4, mid + 2, 2),
                            range(c.bridge_list[1].min_y - 1, c.bridge_list[1].min_y - 4, -1)):
        c.coins_list.append(Obj(x_pos, y_pos, x_pos, y_pos, c.COIN))
    for x_pos, y_pos in zip(range(mid + 2, mid + 8, 2),
                            range(c.bridge_list[1].min_y - 2, c.bridge_list[1].min_y, 1)):
        c.coins_list.append(Obj(x_pos, y_pos, x_pos, y_pos, c.COIN))
    print(c.sub_holes_list[0].max_x, c.sub_holes_list[0].max_y)

    c.coins_list.append(Obj(c.sub_holes_list[0].max_x, c.sub_holes_list[0].max_y,
                            c.sub_holes_list[0].max_x, c.sub_holes_list[0].max_y, c.TIME))
    for x_pos in range(c.holes_list[0].max_x + 5, c.bridge_list[2].min_x - 5, 3):
        c.coins_list.append(Obj(x_pos, up_wall.min_y - 1, x_pos, up_wall.min_y - 1, c.COIN))

    # Create lake and fishes
    min_x = int(8 * c.COLUMNS / 3)
    max_x = int(11 * c.COLUMNS / 3)
    c.lakes.append(Obj(max_x, down_wall.max_y - 1, min_x, up_wall.max_y, c.WATER))
    rand_x = randrange(c.lakes[0].min_x + 2, c.lakes[0].max_x - 2)
    rand_y = c.lakes[0].min_y + randrange(1, 4)
    c.fishes.append(Obj(rand_x, rand_y, rand_x, rand_y, c.FISH))
    rand_x = randrange(c.lakes[0].min_x + 2, c.lakes[0].max_x - 2)
    rand_y = c.lakes[0].min_y + randrange(1, 4)
    c.fishes.append(Obj(rand_x, rand_y, rand_x, rand_y, c.FISH))

    # Generate Clouds
    cloud = print_cloud()
    rand_x = randrange(1, c.COLUMNS)
    rand_x_2 = randrange(c.COLUMNS, 2 * c.COLUMNS)
    rand_x_3 = randrange(2 * c.COLUMNS, 3 * c.COLUMNS)
    c.cloud_list.append(IrregularObjects(len(cloud[0]) + rand_x, 5 + len(cloud), rand_x, 1, cloud))
    c.cloud_list.append(
        IrregularObjects(len(cloud[0]) + rand_x_2, 4 + len(cloud), rand_x_2, 2, cloud))
    c.cloud_list.append(
        IrregularObjects(len(cloud[0]) + rand_x_3, 6 + len(cloud), rand_x_3, 1, cloud))

    # Create Enemies
    c.Enemies_list.append(Enemies(c.sub_holes_list[0].max_x - 2, c.sub_holes_list[0].max_y,
                                  c.sub_holes_list[0].max_x - 3,
                                  c.sub_holes_list[0].max_y - 1, c.ENEMY, c.sub_holes_list[0].min_x,
                                  c.sub_holes_list[0].max_x - 2))
    c.Enemies_list.append(
        Enemies(c.holes_list[1].min_x - 1, up_wall.min_y - 1, c.holes_list[1].min_x - 2,
                up_wall.min_y - 2,
                c.ENEMY, c.bridge_list[2].max_x + 1, c.holes_list[1].min_x - 1))
    c.Enemies_list.append(
        Enemies(c.bridge_list[3].max_x, c.bridge_list[3].min_y - 1, c.bridge_list[3].max_x - 1,
                c.bridge_list[3].min_y - 2, c.ENEMY, c.bridge_list[3].min_x,
                c.bridge_list[3].max_x))

    # Create enemies on bridges on lake
    mid = int((c.lakes[0].min_x + c.lakes[0].max_x) / 2)
    print(c.lakes[0].min_y, c.lakes[0].max_y)
    print('x_pos -> ', c.lakes[0].min_x + 5, mid, 10)
    print('y_pos-> ', c.lakes[0].min_y - 5, c.TOP - 3, int(c.ROWS / 10))
    # sleep(3)
    min_y = int(c.TOP + c.ROWS / 10)
    for x_pos, y_pos in zip(range(c.lakes[0].min_x + 5, mid, 10),
                            range(c.lakes[0].min_y - 5, min_y, -int(c.ROWS / 10))):
        c.bridge_list.append(Obj(x_pos + 3, y_pos, x_pos - 3, y_pos - 1, c.BRIDGE))
        rand_x = randrange(x_pos - 3, x_pos + 3)
        c.Enemies_list.append(
            Enemies(rand_x + 1, y_pos - 2, rand_x, y_pos - 3, c.ENEMY, x_pos - 3, x_pos + 3))
    store = c.bridge_list[-1]
    c.Enemies_list[-1].kill()
    c.Enemies_list.append(Enemies(store.max_x, store.min_y - 1, store.max_x - 1,
                                  store.min_y - 2, c.ENEMY, store.max_x - 1, store.max_x))

    for x_pos, y_pos in zip(range(c.lakes[0].max_x - 5, mid, -10),
                            range(c.lakes[0].min_y - 5, min_y, -int(c.ROWS / 10))):
        c.bridge_list.append(Obj(x_pos + 3, y_pos, x_pos - 3, y_pos - 1, c.BRIDGE))
        rand_x = randrange(x_pos - 3, x_pos + 3)
        c.Enemies_list.append(
            Enemies(rand_x + 1, y_pos - 2, rand_x, y_pos - 3, c.ENEMY, x_pos - 3, x_pos + 3))
    store_2 = c.bridge_list[-1]
    c.bridge_list.append(Obj(store_2.min_x, store.max_y, store.max_x, store.min_y, c.BRIDGE))
    c.Enemies_list[-1].kill()
    c.Enemies_list.append(Enemies(store_2.min_x + 1, store_2.min_y - 1, store_2.min_x,
                                  store_2.min_y - 2, c.ENEMY, store_2.min_x, store_2.min_x + 1))
    mid = int((store.max_x + store_2.min_x) / 2)
    c.life.append(Obj(mid, c.TOP, mid, c.TOP, c.LOVE))

    # Create moving bridges
    min_x = int((11 * c.COLUMNS) / 3) + 7
    length = 15
    max_x = int((9 * c.COLUMNS) / 2)

    # Create Knifes
    c.thrones_list.append(Obj(max_x, up_wall.max_y + 1, min_x, up_wall.max_y, c.THRONES))

    min_y = c.TOP + 5
    max_y = c.lakes[0].min_y - 5
    for x_pos in range(min_x, max_x, 25):
        rand_y = randrange(min_y, max_y + 1)
        c.moving_bridges.append(
            MovingBridges(x_pos + length, rand_y, x_pos, rand_y,
                          c.MOVING_BRIDGES, c.TOP + 5, c.lakes[0].min_y - 5))

    # moving_bridges.append(MovingBridges(lakes[0]))

    # Create the final pole
    c.pole.append(
        Obj(c.MAP_LENGTH - 5, up_wall.min_y - 1, c.MAP_LENGTH - 5, up_wall.min_y - 15, '|'))

    # Declare and start music
    c.control_music.append(Music())
    return up_wall, down_wall


def make_updates():
    """
    Make updates and prints the map to the terminal
    :return:
    """
    global inc

    for stone in c.stones_list:
        temp = Thread(target=stone.move_stone)
        temp.daemon = True
        temp.start()
        if not stone.is_alive:
            c.stones_list.remove(stone)
    if not c.control_music[0].player_crossed_start and c.player[0].min_x > c.holes_list[2].max_x:
        c.control_music[0].player_crossed_start = True
        c.control_music[0].play_music_for_action('Player at lake', change=True)
    if not c.control_music[0].player_crossed_lake and c.player[0].min_x > c.lakes[0].max_x:
        c.control_music[0].player_crossed_lake = True
        c.control_music[0].play_music_for_action('Player at thrones', change=True)
    if not c.control_music[0].player_crossed_thrones and \
            c.player[0].min_x > c.thrones_list[0].max_x:
        c.control_music[0].player_crossed_thrones = True
        c.control_music[0].play_music_for_action('Player at end', change=True)

    rand_x = randrange(1, 100)
    rand_x_2 = randrange(1, 150)
    rand_x_3 = randrange(1, 75)
    if inc % rand_x == 0:
        c.cloud_list[0].move_cloud()
    if inc % rand_x_2 == 0:
        c.cloud_list[1].move_cloud()
    if inc % rand_x_3 == 0:
        c.cloud_list[2].move_cloud()
    inc += 1
    os.system('tput reset')
    fourth = int(c.COLUMNS / 4) - 8

    for i in c.DIMENSIONAL_ARRAY[:]:
        for j in i[c.left_pointer[0]:c.right_pointer[0]]:
            print(j, end='')
        print()
        print('\r', end='')
    print('\r' + c.SCORE_TITLE + ": " + str(c.player[0].score),
          c.TIME + ': ' + str(c.player[0].time), c.LEVEL_I_TITLE,
          c.STONE + ' * ' + str(c.player[0].stones), c.LOVE + ' *' + str(c.player[0].get_lives()),
          sep=' ' * fourth)
    print('\r' + ' ' * c.SPACES_BEFORE_TITLE, c.TITLE)


def launch_stones():
    """
    Launch Stones by the player
    :return:
    """
    if c.player[0].is_alive:
        if c.player[0].stones > 0:
            c.stones_list.append(Stones(c.player[0].max_x + 1, c.player[0].min_y,
                                        c.player[0].max_x + 1, c.player[0].min_y, c.STONE))
            c.player[0].stones -= 1


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
            c.control_music[0].play_music_for_action('Game paused')
            if c.pause.is_set():
                c.pause.clear()
            else:
                c.pause.set()

        if c.player[0].is_alive and not c.pause.is_set() and not c.timeout.is_set():
            if k == 'a':
                c.player[0].move_left()
            elif k == 'd':
                c.player[0].move_right()
            elif k == 'w':
                c.player[0].move_up()
            elif k == 'e':
                c.player[0].move_up_right()
            elif k == 'z':
                c.player[0].move_up_left()
            elif k == 'f':
                launch_stones()


def exit_game():
    """
    Exit the game
    :return:
    """

    os.system("tput cnorm")
    os.system('killall -q aplay 2 >/dev/null')
    os.system('reset')
    last_string = "Thanks for playing my mario game. Your score: " + str(c.player[0].score)
    print(last_string.center(c.COLUMNS))
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
    c.player.append(Players(4, up_wall.min_y - 1, 3, up_wall.min_y - 2, c.PLAYER))

    # Create checkpoints
    c.checkpoints.append((c.player[0].min_x, c.player[0].max_y))
    c.checkpoints.append((c.COLUMNS, up_wall.min_y - 1))
    c.checkpoints.append((c.holes_list[1].max_x + 4, up_wall.min_y - 1))
    c.checkpoints.append((c.holes_list[2].max_x + 4, up_wall.min_y - 1))
    c.checkpoints.append((c.lakes[0].max_x + 1, up_wall.min_y - 1))
    c.control_music[0].play_music_for_action('Player at start')

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
