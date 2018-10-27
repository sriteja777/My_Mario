"""
Contains classes for Movable inherited objects i.e Player, Enemy, Stone, MovingBridge
"""
from threading import Thread
from time import sleep

import config
from objects import MovableObjects


class Players(MovableObjects):
    """
    A class for Player
    """
    def __init__(self, max_x, max_y, min_x, min_y, string):
        """
        Initialise the PLAYER_OBJ
        :param max_x: Maximum x-coordinate of the object
        :param max_y: Minimum y-coordinate of the object
        :param min_x: Maximum x-coordinate of the object
        :param min_y: Minimum y-coordinate of the object
        :param string: String of the PLAYER_OBJ
        """
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)
        self._lives = config.DEFAULT_LIVES
        self.stones = config.DEFAULT_NO_OF_STONES
        self.score = config.INITIAL_SCORE
        self.time = config.DEFAULT_TIMEOUT
        self.check_ends = True

    def move_down(self):
        """
        Moves PLAYER_OBJ down by 1 unit
        :return:
        """
        self.move(100, sign_y=1, vertical=True)

    def move_left(self):
        """
        Moves PLAYER_OBJ left by 1 unit
        :return:
        """
        if self.min_x == 1:
            return
        self.move(1, sign_x=-1, horizontal=True)
        self.move_down()

    def move_right(self):
        """
        Moves PLAYER_OBJ right by 1 unit
        :return:
        """
        if self.max_x == config.MAP_LENGTH:
            return
        self.move(1, sign_x=1, horizontal=True)
        self.move_down()

    def move_up(self, dist=10, down=True):
        """
        Moves PLAYER_OBJ up
        :param dist: Units by which the PLAYER_OBJ should move up
        :param down: boolean whether to move down after moving up
        :return:
        """
        config.CONTROL_MUSIC[0].play_music_for_action('Player jumped')
        self.move(unit=dist, sign_y=-1, vertical=True)
        if down:
            self.move(unit=100, sign_y=1, vertical=True)
            self.move_down()

    def move_up_right(self):
        """
        Moves PLAYER_OBJ simultaneously up and right by 8 units each side
        :return:
        """
        config.CONTROL_MUSIC[0].play_music_for_action('Player jumped')
        self.move(8, sign_x=1, sign_y=-1, horizontal=True, vertical=True)
        self.move(100, sign_x=1, sign_y=1, horizontal=True, vertical=True)
        self.move_down()

    def move_up_left(self):
        """
        Moves PLAYER_OBJ simultaneously up and left by 8 units each side
        :return:
        """
        config.CONTROL_MUSIC[0].play_music_for_action('Player jumped')
        self.move(8, -1, -1, horizontal=True, vertical=True)
        self.move(100, -1, 1, horizontal=True, vertical=True)
        self.move_down()

    def wrong_move(self):
        """
        Called when a Player makes a wrong move
        :return:
        """
        self.remove()
        self.is_alive = False
        # while True:
        #     print('sdfsdf')
        if self._lives == 1:
            config.pause.set()
            config.CONTROL_MUSIC[0].play_music_for_action('Game over', no_thread=True, change=True)
            config.stop.set()
            return
        config.CONTROL_MUSIC[0].play_music_for_action('Player lost LIFE',
                                                      no_thread=True, change=True)
        _new = 'Player at start'
        if self.min_x < config.HOLES_LIST[2].max_x:
            _new = 'Player at start'
        elif self.min_x < config.LAKES[0].max_x:
            _new = 'Player at lake'
        elif self.min_x < config.MAP_LENGTH:
            _new = 'Player at thrones'
        config.CONTROL_MUSIC[0].play_music_for_action(_new, change=True)
        self.update_live(-1)
        for check in config.CHECKPOINTS[-1::-1]:
            if self.max_x >= check[0]:
                self.min_x = check[0]
                self.max_x = check[0] + 1
                self.min_y = check[1] - 1
                self.max_y = check[1]
                break
        if config.left_pointer[0] >= self.min_x - 2:
            config.left_pointer[0] = self.min_x - 2
            config.right_pointer[0] = config.left_pointer[0] + config.COLUMNS
        self.is_alive = True
        self.update()

    def update_live(self, value):
        """
        Increments the lives of PLAYER_OBJ by the given value .
        :param value: value to be incremented
        :return:
        """
        self._lives += value

    def get_lives(self):
        """
        Get number of lives of PLAYER_OBJ
        :return:
        """
        return self._lives

    def clash(self, clashed_with, object_clashed):
        """
        Called when PLAYER_OBJ clashes with a certain object
        :param clashed_with: The string with which it is clashed
        :param object_clashed: The object with which it is clashed
        :return:
        """
        if clashed_with == config.COIN:
            config.CONTROL_MUSIC[0].play_music_for_action('Player got coin')
            # config.pause.set()
            self.score += 1
            return True

        if clashed_with in (config.BRIDGE, config.UP_WALL, config.DOWN_WALL):
            return False
        if clashed_with == config.FLAG_POST:
            config.CONTROL_MUSIC[0].play_music_for_action('Game completed',
                                                          no_thread=True, change=True)
            config.stop.set()

        if clashed_with == config.STONE:
            return False

        if clashed_with == config.ENEMY:
            if self.max_y < object_clashed.min_y:
                config.CONTROL_MUSIC[0].play_music_for_action('Player jumped on enemy')
                self.score += 2
                object_clashed.kill()
                return True
            self.wrong_move()
            return False

        if clashed_with == config.EXTRAS_BRIDGE:
            if self.min_y > object_clashed.max_y:
                config.CONTROL_MUSIC[0].play_music_for_action('Player got power up')
                if object_clashed.bonus == config.LOVE:
                    self.update_live(1)
                elif object_clashed.bonus == config.STONE:
                    self.stones += 1
                elif object_clashed.bonus == config.TIME:
                    self.time += 10
                object_clashed.bonus_taken()
                return False

        if clashed_with == config.LOVE:
            config.CONTROL_MUSIC[0].play_music_for_action('Player got LIFE')
            self.update_live(1)
            return True
        if clashed_with == config.TIME:
            config.CONTROL_MUSIC[0].play_music_for_action('Player got time')
            self.time += 10
            return True
        if clashed_with == config.WATER:
            if not self.max_x == object_clashed.min_x or not self.min_x == object_clashed.max_x:
                self.wrong_move()
                return False
        if clashed_with == config.THRONES:
            self.wrong_move()
        return False


class Stones(MovableObjects):
    """
    Class of stones(i.e bullets)
    """
    def __init__(self, max_x, max_y, min_x, min_y, string):
        """
        Spawns the bullet at position specified by args
        :param max_x: Maximum x-coordinate of the Stone
        :param max_y: Minimum y-coordinate of the Stone
        :param min_x: Maximum x-coordinate of the Stone
        :param min_y: Minimum y-coordinate of the Stone
        :param string: String of the stone
        """
        config.CONTROL_MUSIC[0].play_music_for_action('Player launched stones')
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)

    def move_stone(self):
        """
        Moves the stone based on its current position
        :return:
        """
        if self.max_x >= config.right_pointer[0] or self.min_y > config.SUB_HOLES_LIST[0].max_y:
            self.kill()
            return
        if self.min_y >= config.SUB_HOLES_LIST[0].min_y and \
                self.min_x == config.SUB_HOLES_LIST[0].max_x-1:
            self.kill()
            return
        if config.DIMENSIONAL_ARRAY[self.min_y][self.max_x-1] == config.WATER:
            self.kill()
            return
        if config.DIMENSIONAL_ARRAY[self.min_y][self.max_x-1] == ' ':
            if self.is_alive:
                self.move(1, 1, 1, horizontal=True, vertical=True)

        else:
            if self.is_alive:
                self.move(1, 1, -1, horizontal=True, vertical=True)
        return

    def move_down(self):
        """
        Moves down the stone
        :return:
        """
        self.move(100, sign_y=1, vertical=True)

    def wrong_move(self):
        """
        Called when stone makes a wrong move
        :return:
        """
        pass

    def clash(self, clashed_with, object_clashed):
        """
        Called when stone clashes with a object
        :param clashed_with: The string with which it is clashed
        :param object_clashed: The object with which it is clashed
        :return:
        """
        if clashed_with in (config.BRIDGE, config.COIN, config.FLAG_POST, config.THRONES):
            self.kill()
            return False
        if clashed_with == config.ENEMY:
            config.CONTROL_MUSIC[0].play_music_for_action('Stone hit enemy')
            object_clashed.kill()
            self.kill()
            config.PLAYER_OBJ[0].score += 2
            return False
        return False


class Enemies(MovableObjects):
    """
    Class for enemies in the game
    """
    def __init__(self, max_x, max_y, min_x, min_y, string, range_x1, range_x2):
        """
        Initialises the enemy in the map(DIMENSIONAL_ARRAY)
        :param max_x: Maximum x-coordinate of the object
        :param max_y: Maximum y-coordinate of the object
        :param min_x: Maximum x-coordinate of the object
        :param min_y: Maximum y-coordinate of the object
        :param string: String of the object
        :param range_x1: Minimum x position where the enemy can go up to
        :param range_x2: Maximum x position where the enemy can go up to
        """
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)
        self.range_x1 = range_x1
        self.range_x2 = range_x2

        self.thread = Thread(target=self.move_enemy)
        self.thread.daemon = True
        # sleep(1)
        self.thread.start()

    def wrong_move(self):
        """
        Called when the enemy makes a wrong move
        :return:
        """
        pass

    def move_enemy(self):
        """
        Moves Enemy in between the range
        :return:
        """
        if self.is_alive:
            for _ in range(self.range_x1, self.range_x2):
                if self.min_x > self.range_x1:
                    if self.is_alive:
                        self.move(1, sign_x=-1, horizontal=True)
                        sleep(0.2)
                    else:
                        # self.remove()
                        break
            for _ in range(self.range_x1, self.range_x2):
                if self.max_x < self.range_x2 and self.is_alive:
                    if self.is_alive:
                        self.move(1, sign_x=1, horizontal=True)
                        sleep(0.2)
                    else:
                        # self.remove()
                        break
            self.move_enemy()

    def clash(self, clashed_with, object_clashed):
        """
        Called when the enemy is clashed with an object
        :param clashed_with: The string with which the enemy is clashed
        :param object_clashed: The object with which the enemy is clashed
        :return:
        """
        if clashed_with in (config.BRIDGE, config.UP_WALL, config.DOWN_WALL, config.FLAG_POST):
            return False
        if clashed_with == config.PLAYER:
            object_clashed.wrong_move()
            return False
        return False


class MovingBridges(MovableObjects):
    """
    Class for moving bridges(up and down)
    """
    def __init__(self, max_x, max_y, min_x, min_y, string, range_min, range_max):
        """
        Initialises the moving bridge in the map(DIMENSIONAL_ARRAY)
        :param max_x:
        :param max_y:
        :param min_x:
        :param min_y:
        :param string:
        :param range_min:
        :param range_max:
        """
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)
        self.range_min = range_min
        self.range_max = range_max
        self.thread = Thread(target=self.move_bridge)
        self.thread.daemon = True
        self.thread.start()
        self.going_up = False
        self.going_down = False

    def move_bridge(self):
        """
        Moves the bridge up and down
        :return:
        """
        for _ in range(self.range_min, self.range_max):
            if self.min_y > self.range_min:
                self.going_up = True
                self.check(going_up=True)
                self.move(1, sign_y=-1, vertical=True)
                self.remove()
                self.update()
                sleep(0.2)
            else:
                self.remove()
                self.going_up = False
                break
        for _ in range(self.range_min, self.range_max):
            if self.max_y < self.range_max:
                self.going_down = True
                self.move(1, sign_y=1, vertical=True)
                self.check(down=True)

                sleep(0.2)
            else:
                self.remove()
                self.going_down = False
                break
        self.move_bridge()

    def check(self, going_up=False, down=False):
        """
        Check whether any object is there on the bridge
        :param going_up: Boolean whether bridge is moving up or not
        :param down: Boolean whether bridge is moving down or not
        :return:
        """
        temp = self.max_y - 2
        if down:
            temp -= 1
        if not going_up and not down:
            return
        sign_y = 0
        if going_up:
            sign_y = -1
        if down:
            sign_y = 1

        for i in range(self.min_x, self.max_x+1):
            if not config.DIMENSIONAL_ARRAY[temp][i-1] == ' ':
                config.OBJECT_ARRAY[temp][i-1].move(unit=1, sign_x=0, sign_y=sign_y,
                                                    horizontal=False, vertical=True)

    def wrong_move(self):
        """
        Called when the bridge makes the wrong move
        :return:
        """
        pass

    def clash(self, clashed_with, object_clashed):
        """
        Calls when Bridge is clashed with other object
        :param clashed_with: The string with which the bridge is clashed
        :param object_clashed: The object with which the bridge is clashed
        :return:
        """
        pass
