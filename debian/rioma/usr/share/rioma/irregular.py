"""
Contains classes for Irregular objects
"""

from config import DIMENSIONAL_ARRAY, OBJECT_ARRAY


class IrregularObjects:
    """
    Class for Irregular Objects
    """
    def __init__(self, boundary, lis, map_array=DIMENSIONAL_ARRAY, object_array=OBJECT_ARRAY):
        """
        Initialises the Object parameters in the map
        :param boundary: A dict with initial position of the player having keys
                         max_x, max_y, min_x, min_y
        :param lis: A 2d list of object points
        """
        self.max_x = boundary['max_x']
        self.max_y = boundary['max_y']
        self.min_x = boundary['min_x']
        self.min_y = boundary['min_y']
        self.lis = lis
        self.map_array = map_array
        self.object_array = object_array
        self.update()

    def update(self):
        """
        Updates the object in the map(DIMENSIONAL_ARRAY)
        :return:
        """
        for i in range(self.min_y, self.max_y + 1):
            for j in range(self.min_x, self.max_x + 1):
                try:
                    self.map_array[i-1][j-1] = self.lis[i-self.min_y][j-self.min_x]
                except IndexError:
                    pass

    def remove(self, map_array=DIMENSIONAL_ARRAY):
        """
        Removes the object from the map(DIMENSIONAL_ARRAY)
        :return:
        """
        for i in range(self.min_y+1, self.max_y+1):
            for j in range(self.min_x+1, self.max_x+1):
                try:
                    self.map_array[i-1][j-1] = ' '
                except IndexError:
                    pass

    def move_cloud(self, map_array=DIMENSIONAL_ARRAY):
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
