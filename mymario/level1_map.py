"""
A module containing class for level 1 map
"""

from map import Map


class Level1Map(Map):
    """
    A class for level 1
    """

    def __init__(self, columns, rows, map_length):
        """
        Initialises various attributes of level 1
        :param columns:
        :param rows:
        """
        Map.__init__(self, columns, rows, map_length)
        self.fishes = []
        self.moving_bridges = []
        self.sub_holes = []
        self.thrones = []
        self.clouds = []
        self.lake = ''
        self.stones = []
        self.extras = []
        self.pole = ''
        self.lives = []

    def get_features(self):
        """
        Get Features of map
        :return:
        """
        # Override to print a readable string presentation of your object
        # below is a dynamic way of doing this without explicity constructing the string manually
        return ', '.join(
            ['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in
             self.__dict__]
        )


if __name__ == '__main__':
    TED = Level1Map(1, 2, 10)
    print(TED.get_features())
