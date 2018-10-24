from config import *
from objects import Obj, Extras
from irregular import IrregularObjects, print_cloud
from motion import Players, Stones, Enemies, MovingBridges
from random import randrange
from threading import Thread, Timer
from time import sleep

getch = GetchUnix()
inc = 0
changed_1 = False
changed_2 = False
changed_3 = False


def decrease_time():
    if player[0].time > 0:
        if not pause.is_set():
            player[0].time -= 1

        temp = Timer(1, decrease_time)
        temp.daemon = True
        temp.start()
    else:
        play_music_thread('gameover', change=True, no_thread=True)
        pause.set()
        timeout.set()


def get_extra():
    x = randrange(0, 3)
    if x == 0:
        return TIME
    if x == 1:
        return LOVE
    if x == 2:
        return STONE


def create_level1_map():
    # Create the ground for the player
    down_wall = Obj(MAP_LENGTH, ROWS, 1, int((9 * ROWS) / 10), DOWN_WALL)
    up_wall = Obj(MAP_LENGTH, down_wall.min_y - 1, 1, down_wall.min_y - 1, UP_WALL)

    # Create bridges(some at random place and some at predefined place)
    bridge_list.append(Obj(20, up_wall.min_y - 5, 14, up_wall.min_y - 7, BRIDGE))
    bridge_list.append(Obj(40, up_wall.min_y - 5, 25, up_wall.min_y - 7, BRIDGE))
    bridge_list.append(Obj(COLUMNS - 4, up_wall.min_y - 1, COLUMNS - 10, up_wall.min_y - 7, BRIDGE))
    rand_x = randrange(COLUMNS + 5, int(4 * COLUMNS / 3) - 5)
    bridge_list.append(Obj(5 + rand_x, up_wall.min_y - 5, rand_x - 5, up_wall.min_y - 8, BRIDGE))
    rand_x = randrange(int(5 * COLUMNS / 3) + 1, 2 * COLUMNS - 2)
    bridge_list.append(Obj(rand_x + 1, up_wall.min_y - 6, rand_x - 1, up_wall.min_y - 8, BRIDGE))
    rand_x = randrange(2 * COLUMNS + 6, int((7 * COLUMNS) / 3) - 6)
    cross_bridge_list = [[' ' for _ in range(0, 15)] for _ in range(0, 15)]
    for i in range(0, 15):
        for j in range(15 - i, 15):
            cross_bridge_list[i][j] = BRIDGE
    bridge_list.append(IrregularObjects(rand_x + 6, up_wall.min_y - 1, rand_x - 6,
                                        up_wall.min_y - 14, cross_bridge_list))

    # Create extras
    mid = int((bridge_list[1].min_x + bridge_list[1].max_x)/2)
    extras.append(Extras(mid+1, bridge_list[1].max_y, mid-1, bridge_list[1].min_y, EXTRAS_BRIDGE, get_extra()))
    mid = int((bridge_list[3].min_x + bridge_list[3].max_x) / 2)
    extras.append(Extras(mid+1, bridge_list[3].max_y, mid-1, bridge_list[3].min_y, EXTRAS_BRIDGE, get_extra()))

    # Create holes
    rand_x = randrange(int(COLUMNS / 3), int((2 * COLUMNS) / 3))
    print(down_wall.max_y-2)
    print(len(DIMENSIONAL_ARRAY))
    holes_list.append(Obj(rand_x + 5, down_wall.max_y-2, rand_x, up_wall.min_y, ' '))
    sub_holes_list.append(Obj(holes_list[0].max_x + 10, holes_list[0].max_y,
                              holes_list[0].min_x, up_wall.min_y+2, ' '))
    rand_x = randrange(int((4 * COLUMNS) / 3) + 4, int(5 * COLUMNS / 3) - 4)
    holes_list.append(Obj(rand_x + 4, ROWS, rand_x - 4, up_wall.min_y, ' '))
    holes_list.append(Obj(bridge_list[5].max_x + 24, ROWS, bridge_list[5].max_x + 1, up_wall.min_y, ' '))

    # Create Coins
    mid = int((bridge_list[0].min_x + bridge_list[0].max_x) / 2)
    coins_list.append(Obj(mid, bridge_list[0].min_y - 1, mid, bridge_list[0].min_y - 1, COIN))
    mid = int((bridge_list[1].min_x + bridge_list[1].max_x) / 2)
    for i, j in zip(range(mid - 4, mid + 2, 2), range(bridge_list[1].min_y - 1, bridge_list[1].min_y - 4, -1)):
        coins_list.append(Obj(i, j, i, j, COIN))
    for i, j in zip(range(mid + 2, mid + 8, 2), range(bridge_list[1].min_y - 2, bridge_list[1].min_y, 1)):
        coins_list.append(Obj(i, j, i, j, COIN))
    print(sub_holes_list[0].max_x, sub_holes_list[0].max_y)

    coins_list.append(Obj(sub_holes_list[0].max_x, sub_holes_list[0].max_y,
                          sub_holes_list[0].max_x, sub_holes_list[0].max_y, TIME))
    for i in range(holes_list[0].max_x + 5, bridge_list[2].min_x - 5, 3):
        coins_list.append(Obj(i, up_wall.min_y - 1, i, up_wall.min_y - 1, COIN))

    # Create lake and fishes
    min_x = int(8 * COLUMNS / 3)
    max_x = int(11 * COLUMNS / 3)
    lakes.append(Obj(max_x, down_wall.max_y-1, min_x, up_wall.max_y, WATER))
    rand_x = randrange(lakes[0].min_x+2, lakes[0].max_x-2)
    rand_y = lakes[0].min_y + randrange(1, 4)
    fishes.append(Obj(rand_x, rand_y, rand_x, rand_y, FISH))
    rand_x = randrange(lakes[0].min_x + 2, lakes[0].max_x - 2)
    rand_y = lakes[0].min_y + randrange(1, 4)
    fishes.append(Obj(rand_x, rand_y, rand_x, rand_y, FISH))

    # Generate Clouds
    cloud = print_cloud()
    rand_x = randrange(1, COLUMNS)
    rand_x_2 = randrange(COLUMNS, 2 * COLUMNS)
    rand_x_3 = randrange(2 * COLUMNS, 3 * COLUMNS)
    cloud_list.append(IrregularObjects(len(cloud[0]) + rand_x, 5 + len(cloud), rand_x, 1, cloud))
    cloud_list.append(IrregularObjects(len(cloud[0]) + rand_x_2, 4 + len(cloud), rand_x_2, 2, cloud))
    cloud_list.append(IrregularObjects(len(cloud[0]) + rand_x_3, 6 + len(cloud), rand_x_3, 1, cloud))

    # Create Enemies
    Enemies_list.append(Enemies(sub_holes_list[0].max_x-2, sub_holes_list[0].max_y, sub_holes_list[0].max_x - 3,
                                sub_holes_list[0].max_y - 1, ENEMY, sub_holes_list[0].min_x, sub_holes_list[0].max_x-2))
    Enemies_list.append(Enemies(holes_list[1].min_x - 1, up_wall.min_y - 1, holes_list[1].min_x - 2, up_wall.min_y - 2,
                                ENEMY, bridge_list[2].max_x + 1, holes_list[1].min_x - 1))
    Enemies_list.append(Enemies(bridge_list[3].max_x, bridge_list[3].min_y - 1, bridge_list[3].max_x - 1,
                                bridge_list[3].min_y - 2, ENEMY, bridge_list[3].min_x, bridge_list[3].max_x))

    # Create enemies on bridges on lake
    mid = int((lakes[0].min_x + lakes[0].max_x) / 2)
    print(lakes[0].min_y, lakes[0].max_y)
    print('x -> ', lakes[0].min_x + 5, mid, 10)
    print('y-> ', lakes[0].min_y - 5, TOP - 3, int(ROWS / 10))
    # sleep(3)
    min_y = int(TOP + ROWS / 10)
    for x, y in zip(range(lakes[0].min_x + 5, mid, 10), range(lakes[0].min_y - 5, min_y, -int(ROWS / 10))):
        bridge_list.append(Obj(x + 3, y, x - 3, y - 1, BRIDGE))
        rand_x = randrange(x-3, x+3)
        Enemies_list.append(Enemies(rand_x+1, y - 2, rand_x, y - 3, ENEMY, x - 3, x + 3))
    store = bridge_list[-1]
    Enemies_list[-1].kill()
    Enemies_list.append(Enemies(store.max_x, store.min_y-1, store.max_x-1,
                                store.min_y-2, ENEMY, store.max_x-1, store.max_x))

    for x, y in zip(range(lakes[0].max_x - 5, mid, -10), range(lakes[0].min_y - 5, min_y, -int(ROWS / 10))):
        bridge_list.append(Obj(x + 3, y, x - 3, y - 1, BRIDGE))
        rand_x = randrange(x - 3, x + 3)
        Enemies_list.append(Enemies(rand_x+1, y - 2, rand_x, y - 3, ENEMY, x - 3, x + 3))
    store_2 = bridge_list[-1]
    bridge_list.append(Obj(store_2.min_x, store.max_y, store.max_x, store.min_y, BRIDGE))
    Enemies_list[-1].kill()
    Enemies_list.append(Enemies(store_2.min_x+1, store_2.min_y - 1, store_2.min_x,
                                store_2.min_y - 2, ENEMY, store_2.min_x, store_2.min_x+1))
    mid = int((store.max_x + store_2.min_x)/2)
    life.append(Obj(mid, TOP, mid, TOP, LOVE))

    # Create moving bridges
    min_x = int((11*COLUMNS)/3) + 7
    length = 15
    max_x = int((9*COLUMNS)/2)

    # Create Knifes
    thrones_list.append(Obj(max_x, up_wall.max_y+1, min_x, up_wall.max_y, THRONES))

    min_y = TOP + 5
    max_y = lakes[0].min_y - 5
    for x in range(min_x, max_x, 25):
        rand_y = randrange(min_y, max_y+1)
        moving_bridges.append(
            MovingBridges(x+length, rand_y, x, rand_y,
                          MOVING_BRIDGES, TOP + 5, lakes[0].min_y - 5))

    # moving_bridges.append(MovingBridges(lakes[0]))

    # Create the final pole
    pole.append(Obj(MAP_LENGTH - 5, up_wall.min_y - 1, MAP_LENGTH - 5, up_wall.min_y - 15, '|'))
    return up_wall, down_wall


def make_updates():
    global inc
    global changed_2, changed_1, changed_3
    for stone in stones_list:
        temp = Thread(target=stone.move_stone)
        temp.daemon = True
        temp.start()
        if not stone.is_alive:
            stones_list.remove(stone)
    if not changed_1 and player[0].min_x > holes_list[2].max_x:
        changed_1 = True
        play_music_thread('lake', change=True)
    if not changed_2 and player[0].min_x > lakes[0].max_x:
        changed_2 = True
        play_music_thread('last', change=True)
    if not changed_3 and player[0].min_x > thrones_list[0].max_x:
        changed_3 = True
        play_music_thread('ending', change=True)
    # if not player[0].going_up:
    # player[0].move_down()
    rand_x = randrange(1, 100)
    rand_x_2 = randrange(1, 150)
    rand_x_3 = randrange(1, 75)
    if inc % rand_x == 0:
        cloud_list[0].move_cloud()
    if inc % rand_x_2 == 0:
        cloud_list[1].move_cloud()
    if inc % rand_x_3 == 0:
        cloud_list[2].move_cloud()
    inc += 1
    os.system('tput reset')
    fourth = int(COLUMNS/4)-8

    for i in DIMENSIONAL_ARRAY[:]:
        for j in i[left_pointer[0]:right_pointer[0]]:
            print(j, end='')
        print()
        print('\r', end='')
    print('\r' + SCORE_TITLE + ": " + str(player[0].score), TIME + ': ' + str(player[0].time), LEVEL_I_TITLE,
          STONE + ' * ' + str(player[0].stones), LOVE + ' *' + str(player[0]._lives), sep=' ' * fourth)
    print('\r'+' ' * SPACES_BEFORE_TITLE, TITLE)


def launch_stones():
    if player[0].is_alive:
        if player[0].stones > 0:
            stones_list.append(Stones(player[0].max_x + 1, player[0].min_y,
                                      player[0].max_x + 1, player[0].min_y, STONE))
            player[0].stones -= 1


def get_input():
    while True:
        k = getch()
        if k == 'q':
            stop.set()
            break

        if k == ' ':
            # pause the game
            play_music_thread('pause')
            if pause.is_set():
                pause.clear()
            else:

                pause.set()

        if player[0].is_alive and not pause.is_set() and not timeout.is_set():
            if k == 'a':
                player[0].move_left()
            elif k == 'd':
                player[0].move_right()
            elif k == 'w':
                player[0].move_up()
            elif k == 'e':
                player[0].move_up_right()
            elif k == 'z':
                player[0].move_up_left()
            elif k == 'f':
                launch_stones()
            elif k == 't':
                # left_pointer[0] -= 10
                # right_pointer[0] -= 10
                sleep(2)
                player[0].wrong_move()
                sleep(10)


def exit_game():
    """
    Exit the game
    :return:
    """

    os.system("tput cnorm")
    os.system('killall -q aplay 2 >/dev/null')
    os.system('reset')
    last_string = "Thanks for playing my mario game. Your score: " + str(player[0].score)
    print(last_string.center(COLUMNS))
    exit(0)


# Initial Interactive
def start_screen():
    try:
        os.system('clear')
        os.system('tput civis')
        print('Hi!, Welcome to "My Mario" Game'.center(COLUMNS))
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


start_screen()
# Initiate the screen
Obj(COLUMNS, ROWS, 1, 3, ' ')
up_wall, down_wall = create_level1_map()
player.append(Players(4, up_wall.min_y - 1, 3, up_wall.min_y - 2, PLAYER))

# Create checkpoints
checkpoints.append((player[0].min_x, player[0].max_y))
checkpoints.append((COLUMNS, up_wall.min_y-1))
checkpoints.append((holes_list[1].max_x+4, up_wall.min_y-1))
checkpoints.append((holes_list[2].max_x+4, up_wall.min_y-1))
checkpoints.append((lakes[0].max_x+1, up_wall.min_y-1))
play_music_thread('start')

make_updates()
inp_thread = Thread(target=get_input)
inp_thread.daemon = True
inp_thread.start()
time_thread = Thread(target=decrease_time)
time_thread.daemon = True
time_thread.start()


while True:
    try:
        if stop.is_set() or timeout.is_set():
            break
        sleep(0.1)
        make_updates()

    except KeyboardInterrupt:
        break

exit_game()
