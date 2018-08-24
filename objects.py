import config
from time import sleep
from abc import ABC, abstractmethod


class Obj:
    def __init__(self, max_x, max_y, min_x, min_y, string):
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.string = string
        self.update_dimensional_array()
        self.check_ends = False

    def update_dimensional_array(self):
        for i in range(self.min_y, self.max_y + 1):
            for j in range(self.min_x, self.max_x+1):
                if self.string:
                    config.DIMENSIONAL_ARRAY[i-1][j-1] = self.string
                    config.OBJECT_ARRAY[i-1][j-1] = self

    def update(self):
        self.update_dimensional_array()

    def remove(self):
        for i in range(self.min_y, self.max_y + 1):
            for j in range(self.min_x, self.max_x+1):
                config.DIMENSIONAL_ARRAY[i-1][j-1] = ' '
                config.OBJECT_ARRAY[i-1][j-1] = self


class MovableObjects(Obj, ABC):
    def __init__(self, max_x, max_y, min_x, min_y, string):
        Obj.__init__(self,  max_x, max_y, min_x, min_y, string)
        self.is_alive = True

    @abstractmethod
    def clash(self, clashed_with, object_clashed):
        pass

    def move(self, unit=1, sign_x=0, sign_y=0, horizontal=False, vertical=False, update=True):
        if not horizontal and not vertical:
            return

        while unit > 0:
            if config.pause.is_set():
                while True:
                    sleep(1)
                    if not config.pause.is_set():
                        break

            temp2 = self.min_x
            temp3 = self.max_x
            temp4 = self.min_y
            temp5 = self.max_y
            if update:
                self.remove()

            if horizontal:
                temp2 = self.min_x + sign_x
                temp3 = self.max_x + sign_x
            if vertical:
                temp4 = self.min_y + sign_y
                temp5 = self.max_y + sign_y
            if self.check_ends:
                if temp5 >= config.ROWS:
                    self.wrong_move()
                    break
                if temp3 > config.right_pointer[0] or temp2 <= config.left_pointer[0]:
                    if update:
                        self.update()
                    break

            if temp4 < config.TOP:
                if update:
                    self.update()
                break
            flag = True
            clashed_with = ''
            object_clashed = ''

            for i in range(temp4, temp5+1):
                for j in range(temp2, temp3+1):
                    if horizontal and vertical:
                        pass
                    if not config.DIMENSIONAL_ARRAY[i-1][j-1] == ' ':
                        flag = False
                        clashed_with = config.DIMENSIONAL_ARRAY[i-1][j-1]
                        object_clashed = config.OBJECT_ARRAY[i-1][j-1]

            mrn = True
            if not flag:
                mrn = False
                try:
                    mrn = self.clash(clashed_with, object_clashed)
                except AttributeError:
                    pass
            if mrn:
                mid = (config.left_pointer[0] + config.right_pointer[0])/2
                if len(config.player) > 0:
                    if self == config.player[0] and horizontal and temp2 > self.min_x > mid:
                        if config.right_pointer[0] < config.MAP_LENGTH:
                            config.left_pointer[0] += 1
                            config.right_pointer[0] += 1
                self.min_x = temp2
                self.max_x = temp3
                self.min_y = temp4
                self.max_y = temp5
                if update:
                    self.update()

            else:
                if self.is_alive:
                    self.update()
                break
            if update:
                self.update()
            unit = unit - 1
            if vertical:
                if sign_y == -1:
                    sleep((10 - unit)/100)
                else:
                    sleep((unit % 10)/100)

    def kill(self):
        self.is_alive = False
        self.remove()


class Extras(Obj):
    def __init__(self, max_x, max_y, min_x, min_y, string, bonus):
        Obj.__init__(self, max_x, max_y, min_x, min_y, string)
        self.bonus = bonus

    def bonus_taken(self):
        self.string = config.BRIDGE
        self.update()
