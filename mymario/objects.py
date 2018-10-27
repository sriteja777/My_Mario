"""
Contains Classes for movable and for non-movable regular objects
"""

from abc import ABC, abstractmethod
from time import sleep

import config


class Obj:
    """
    A class for all regular objects
    """
    def __init__(self, max_x, max_y, min_x, min_y, string):
        """
        Initialises the Object in the map in the given boundary with the given string
        :param max_x: Maximum x-coordinate of the object
        :param max_y: Maximum y-coordinate of the object
        :param min_x: Minimum x-coordinate of the object
        :param min_y: Minimum y-coordinate of the object
        :param string: The boundary to be filled with
        """
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.string = string
        self.update_dimensional_array()
        self.check_ends = False

    def update_dimensional_array(self):
        """
        Updates the object in  the map(DIMENSIONAL_ARRAY)
        :return:
        """
        for i in range(self.min_y, self.max_y + 1):
            for j in range(self.min_x, self.max_x+1):
                if self.string:
                    config.DIMENSIONAL_ARRAY[i-1][j-1] = self.string
                    config.OBJECT_ARRAY[i-1][j-1] = self

    def update(self):
        """
        Updates the object in  the map(DIMENSIONAL_ARRAY)
        :return:
        """
        self.update_dimensional_array()

    def remove(self):
        """
        Removes the object from the map(DIMENSIONAL_ARRAY)
        :return:
        """
        for i in range(self.min_y, self.max_y + 1):
            for j in range(self.min_x, self.max_x+1):
                config.DIMENSIONAL_ARRAY[i-1][j-1] = ' '
                config.OBJECT_ARRAY[i-1][j-1] = self


class MovableObjects(Obj, ABC):
    """
    A class for movable regular objects
    """
    def __init__(self, max_x, max_y, min_x, min_y, string):
        """
        Initialises the Movable Object in the map in the given boundary with the given string
        :param max_x: Maximum x-coordinate of the object
        :param max_y: Minimum y-coordinate of the object
        :param min_x: Maximum x-coordinate of the object
        :param min_y: Minimum y-coordinate of the object
        :param string: The boundary to be filled with
        """
        Obj.__init__(self, max_x, max_y, min_x, min_y, string)
        self.is_alive = True

    @abstractmethod
    def clash(self, clashed_with, object_clashed):
        """
        An Abstract method called when an object is clashed with other.
        It has to be implemented by the class who inherits it
        :param clashed_with: The string with which it is clashed
        :param object_clashed: The object with which it is clashed
        :return:
        """
        pass

    @abstractmethod
    def wrong_move(self):
        """
        An Abstract method called when a movable object makes a wrong move.
        It has to be implemented by the class who inherits it
        :return:
        """
        pass

    def move(self, unit=1, sign_x=0, sign_y=0, horizontal=False, vertical=False, update=True):
        """
        A method to move the object
        :param unit: Number of units to move
        :param sign_x: Horizontal direction of movement
        :param sign_y: Vertical direction of movement
        :param horizontal: boolean whether to move horizontal or not
        :param vertical: boolean whether to move horizontal or not
        :param update: boolean whether to update the movement or not
        :return:
        """
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
                if config.player:
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
        """
        Kills the object from the game. It cannot take re-birth
        :return:
        """
        self.is_alive = False
        self.remove()


class Extras(Obj):
    """
    A class for bonus points in the bridges.
    """
    def __init__(self, max_x, max_y, min_x, min_y, string, bonus):
        """
        Initialises the Bonus Object in the map in the given boundary with the given string
        :param max_x: Maximum x-coordinate of the object
        :param max_y: Minimum y-coordinate of the object
        :param min_x: Maximum x-coordinate of the object
        :param min_y: Minimum y-coordinate of the object
        :param string: The boundary to be filled with
        :param bonus: Bonus Point
        """
        Obj.__init__(self, max_x, max_y, min_x, min_y, string)
        self.bonus = bonus

    def bonus_taken(self):
        """
        Called when the bonus is taken by user
        :return:
        """
        self.string = config.BRIDGE
        self.update()
