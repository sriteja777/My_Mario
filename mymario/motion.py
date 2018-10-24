from objects import *
import config
from threading import Thread
from os import system


class Players(MovableObjects):
    def __init__(self, max_x, max_y, min_x, min_y, string):
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)
        self._lives = config.DEFAULT_LIVES
        self.stones = config.DEFAULT_NO_OF_STONES
        self.score = config.INITIAL_SCORE
        self.time = config.DEFAULT_TIMEOUT
        self.check_ends = True

    def move_down(self):
        self.move(100, sign_y=1, vertical=True)

    def move_left(self):
        if self.min_x == 1:
            return
        self.move(1, sign_x=-1, horizontal=True)
        self.move_down()

    def move_right(self):
        if self.max_x == config.MAP_LENGTH:
            return
        self.move(1, sign_x=1, horizontal=True)
        self.move_down()

    def move_up(self, dist=10, down=True):
        config.play_music_thread('jump')
        self.move(unit=dist, sign_y=-1, vertical=True)
        if down:
            self.move(unit=100, sign_y=1, vertical=True)
            self.move_down()

    def move_up_right(self):
        config.play_music_thread('jump')
        self.move(8, sign_x=1, sign_y=-1, horizontal=True, vertical=True)
        self.move(100, sign_x=1, sign_y=1, horizontal=True, vertical=True)
        self.move_down()

    def move_up_left(self):
        config.play_music_thread('jump')
        self.move(8, -1, -1, horizontal=True, vertical=True)
        self.move(100, -1, 1, horizontal=True, vertical=True)
        self.move_down()

    def wrong_move(self):
        self.remove()
        self.is_alive = False
        # while True:
        #     print('sdfsdf')
        if self._lives == 1:
            config.pause.set()
            config.play_music_thread('gameover', no_thread=True, change=True)
            config.stop.set()
            return
        config.play_music_thread('lostlife', no_thread=True, change=True)
        if self.min_x < config.holes_list[2].max_x:
            _new = 'start'
        elif self.min_x < config.lakes[0].max_x:
            _new = 'lake'
        elif self.min_x < config.MAP_LENGTH:
            _new = 'last'
        config.play_music_thread(_new, change=True)
        self.update_live(-1)
        for check in config.checkpoints[-1::-1]:
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
        self._lives += value

    def clash(self, clashed_with, object_clashed):
        if clashed_with == config.COIN:
            config.play_music_thread('coin')
            self.score += 1
            return True

        if clashed_with == config.BRIDGE or clashed_with == config.UP_WALL or clashed_with == config.DOWN_WALL:
            return False
        if clashed_with == config.FLAG_POST:
            config.play_music_thread('finished', no_thread=True, change=True)
            config.stop.set()

        if clashed_with == config.STONE:
            return False

        if clashed_with == config.ENEMY:
            if self.max_y < object_clashed.min_y:
                config.play_music_thread('jumponenemy')
                self.score += 2
                object_clashed.kill()
                return True
            else:
                self.wrong_move()
                pass
            return False

        if clashed_with == config.EXTRAS_BRIDGE:

            if self.min_y > object_clashed.max_y:
                config.play_music_thread('powerup')
                if object_clashed.bonus == config.LOVE:
                    # self._lives += 1
                    self.update_live(1)
                elif object_clashed.bonus == config.STONE:
                    self.stones += 1
                elif object_clashed.bonus == config.TIME:
                    self.time += 10
                object_clashed.bonus_taken()
                return False

        if clashed_with == config.LOVE:
            config.play_music_thread('gotlife')
            self.update_live(1)
            return True
        if clashed_with == config.TIME:
            config.play_music_thread('gottime')
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
    def __init__(self, max_x, max_y, min_x, min_y, string):
        config.play_music_thread('stones')
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)

    def move_stone(self):
        if self.max_x >= config.right_pointer[0] or self.min_y > config.sub_holes_list[0].max_y:
            self.kill()
            return
        if self.min_y >= config.sub_holes_list[0].min_y and self.min_x == config.sub_holes_list[0].max_x-1:
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
        return 0

    def move_down(self):
        self.move(100, sign_y=1, vertical=True)

    def wrong_move(self):
        pass

    def clash(self, clash_with, object_clashed):
        if clash_with == config.BRIDGE or clash_with == config.COIN or clash_with == config.FLAG_POST or clash_with == config.THRONES:
            self.kill()
            return False
        if clash_with == config.ENEMY:
            config.play_music_thread('stoneonenemy')
            object_clashed.kill()
            self.kill()
            config.player[0].score += 2
            return False
        return False


class Enemies(MovableObjects):
    def __init__(self, max_x, max_y, min_x, min_y, string, range_x1, range_x2):
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)
        self.range_x1 = range_x1
        self.range_x2 = range_x2

        self.thread = Thread(target=self.move_enemy)
        self.thread.daemon = True
        # sleep(1)
        self.thread.start()

    def wrong_move(self):
        pass

    def move_enemy(self):
        if self.is_alive:
            for i in range(self.range_x1, self.range_x2):
                if self.min_x > self.range_x1:
                    if self.is_alive:
                        self.move(1, sign_x=-1, horizontal=True)
                        sleep(0.2)
                    else:
                        # self.remove()
                        break
            for i in range(self.range_x1, self.range_x2):
                if self.max_x < self.range_x2 and self.is_alive:
                    if self.is_alive:
                        self.move(1, sign_x=1, horizontal=True)
                        sleep(0.2)
                    else:
                        # self.remove()
                        break
            self.move_enemy()

    def clash(self, clashed_with, object_clashed):
        if clashed_with == config.BRIDGE or clashed_with == config.UP_WALL or clashed_with == config.DOWN_WALL or clashed_with == config.FLAG_POST:
            return False
        if clashed_with == config.PLAYER:
            object_clashed.wrong_move()
            return False
        return False


class MovingBridges(MovableObjects):
    def __init__(self, max_x, max_y, min_x, min_y, string, range_min, range_max):
        MovableObjects.__init__(self, max_x, max_y, min_x, min_y, string)
        self.range_min = range_min
        self.range_max = range_max
        self.thread = Thread(target=self.move_bridge)
        self.thread.daemon = True
        self.thread.start()
        self.going_up = False
        self.going_down = False

    def move_bridge(self):
        for i in range(self.range_min, self.range_max):
            if self.min_y > self.range_min:
                self.going_up = True
                self.check(up=True)
                self.move(1, sign_y=-1, vertical=True)
                self.remove()
                self.update()
                sleep(0.2)
            else:
                self.remove()
                self.going_up = False
                break
        for i in range(self.range_min, self.range_max):
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

    def check(self, up=False, down=False):
        temp = self.max_y - 2
        if down:
            temp -= 1
        if not up and not down:
            return
        y = 0
        if up:
            y = -1
        if down:
            y = 1

        for i in range(self.min_x, self.max_x+1):
            if not config.DIMENSIONAL_ARRAY[temp][i-1] == ' ':
                config.OBJECT_ARRAY[temp][i-1].move(unit=1, sign_x=0, sign_y=y, horizontal=False, vertical=True)

    def wrong_move(self):
        pass

    def clash(self, clashed_with, object_clashed):
        pass
