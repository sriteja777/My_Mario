from random import randrange

from irregular import print_cloud, IrregularObjects
from map import Map
from motion import MovingBridges, Enemies
from objects import Obj, Extras
import config


class TestMap(Map):
    def __init__(self, map_id, rows, columns):
        Map.__init__(self, map_id, columns, rows, columns)
        self.up_wall = None
        self.down_wall = None
        self.create_walls()
        self.clouds = []
        self.initial_player_position = [{'max_x': 4, 'max_y': self.up_wall.min_y - 1, 'min_x': 3,
                                        'min_y': self.up_wall.min_y - 2},
                                        {'max_x': 20, 'max_y': self.up_wall.min_y - 1, 'min_x': 19,
                                        'min_y': self.up_wall.min_y - 2}]
        self.create_clouds()

    def create_walls(self):
        # Dependencies: None

        self.down_wall = Obj(self.length, self.rows, 1, int((9 * self.rows) / 10), config.DOWN_WALL,
                             self.map_array, self.object_array)
        self.up_wall = Obj(self.length, self.down_wall.min_y - 1, 1, self.down_wall.min_y - 1,
                           config.UP_WALL, self.map_array, self.object_array)

    def create_clouds(self):
        # Dependencies: None

        cloud = print_cloud()
        rand_x = randrange(1, self.columns)
        rand_x_2 = randrange(self.columns, 2 * self.columns)
        rand_x_3 = randrange(2 * self.columns, 3 * self.columns)
        self.clouds.append(IrregularObjects(
            {'max_x': len(cloud[0]) + rand_x, 'max_y': 5 + len(cloud), 'min_x': rand_x, 'min_y': 1},
            cloud, self.map_array, self.object_array))
        self.clouds.append(IrregularObjects(
            {'max_x': len(cloud[0]) + rand_x_2, 'max_y': 4 + len(cloud), 'min_x': rand_x_2,
             'min_y': 2},
            cloud, self.map_array, self.object_array))
        self.clouds.append(IrregularObjects(
            {'max_x': len(cloud[0]) + rand_x_3, 'max_y': 6 + len(cloud), 'min_x': rand_x_3,
             'min_y': 1},
            cloud, self.map_array, self.object_array))


