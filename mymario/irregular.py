"""
Contains classes for Irregular objects
"""

from config import DIMENSIONAL_ARRAY


class IrregularObjects:
    """
    Class for Irregular Objects
    """
    def __init__(self, max_x, max_y, min_x, min_y, lis):
        """
        Initialises the Object parameters in the map(DIMENSIONAL_ARRAY)
        :param max_x: Maximum x-coordinate of the object
        :param max_y: Minimum y-coordinate of the object
        :param min_x: Maximum x-coordinate of the object
        :param min_y: Minimum y-coordinate of the object
        :param lis: A 2d list of object points
        """
        self.max_x = max_x
        self.max_y = max_y
        self.min_x = min_x
        self.min_y = min_y
        self.lis = lis
        self.update()

    def update(self):
        """
        Updates the object in the map(DIMENSIONAL_ARRAY)
        :return:
        """
        for i in range(self.min_y, self.max_y + 1):
            for j in range(self.min_x, self.max_x + 1):
                try:
                    DIMENSIONAL_ARRAY[i-1][j-1] = self.lis[i-self.min_y][j-self.min_x]
                except IndexError:
                    pass

    def remove(self):
        """
        Removes the object from the map(DIMENSIONAL_ARRAY)
        :return:
        """
        for i in range(self.min_y+1, self.max_y+1):
            for j in range(self.min_x+1, self.max_x+1):
                try:
                    DIMENSIONAL_ARRAY[i-1][j-1] = ' '
                except IndexError:
                    pass

    def move_cloud(self):
        """
        Moves the Irregular Object
        :return:
        """
        self.remove()
        self.min_x -= 1
        self.max_x -= 1
        self.update()


def print_cloud():
    """
    Break down the string of irregular object to a 2d list
    :return:
    """
    cloud_str = r'''
    _/\  /\/\/\  /^\  
    \  \/      \/   \ 
    /               / 
    \______________/  
    '''

    # cloud_str = COLORS['Light Grey'] + '''
    # _/\  /\/\/\  /^\
    # \  \/      \/   \
    # /               /
    # \______________/
    # ''' + END_COLOR
    cloud_list = []
    temp = []
    i = 0
    while i < len(cloud_str):
        if cloud_str[i] == '\n':
            i += 4
            if temp:
                cloud_list.append(temp)
                temp = []
        else:
            temp.append(cloud_str[i])
        i += 1

    # for i in CLOUD_LIST:
    #     for j in i:
    #         print(j, end='')
    #     print()
    return cloud_list
