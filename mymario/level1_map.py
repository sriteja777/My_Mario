"""
A module containing class for level 1 map
"""
from random import randrange

from irregular import print_cloud, IrregularObjects
from map import Map
from motion import MovingBridges, Enemies
from objects import Obj, Extras
import config


def get_extra():
    """
    Returns any random extra point when PLAYER_OBJ touches extra bridges
    :return: Returns the string of extra point
    """
    num = randrange(0, 3)
    if num == 0:
        return config.TIME
    if num == 1:
        return config.LOVE
    # x = 2
    return config.STONE


class Level1Map(Map):
    """
    A class for level 1
    """

    def __init__(self, map_id, rows, columns):
        """
        Initialises various attributes of level 1
        :param columns:
        :param rows:
        """

        Map.__init__(self, map_id, columns, rows, 5*columns)
        self.fishes = []
        self.moving_bridges = []
        self.sub_holes = []
        self.thrones = []
        self.clouds = []
        self.lake = None
        self.stones = []
        self.extras = []
        self.pole = None
        self.lives = []
        self.up_wall = None
        self.down_wall = None
        print(self.length, self.columns, self.rows)
        print(config.MAP_LENGTH, config.COLUMNS, config.ROWS)
        self.create_walls()
        self.create_clouds()
        self.create_pole()
        self.create_lake_fishes()
        self.create_bridges()
        self.create_moving_bridges()
        self.create_holes()
        self.create_coins()
        self.create_enemies()
        self.create_extras()
        self.initial_player_position = {'max_x': 4, 'max_y': self.up_wall.min_y - 1, 'min_x': 3, 'min_y': self.up_wall.min_y - 2}
        self.create_checkpoints()

    def create_checkpoints(self):
        """
        Dependencies: initial player position, walls, holes, lakes
        :return:
        """
        self.checkpoints.append((self.initial_player_position['min_x'], self.initial_player_position['max_y']))
        self.checkpoints.append((self.columns, self.up_wall.min_y - 1))
        self.checkpoints.append((self.holes[1].max_x + 4, self.up_wall.min_y - 1))
        self.checkpoints.append((self.holes[2].max_x + 4, self.up_wall.min_y - 1))
        self.checkpoints.append((self.lake.max_x + 1, self.up_wall.min_y - 1))

    def create_enemies(self):
        """
        Dependencies: Holes, bridges, lakes, walls
        """
        self.enemies.append(Enemies(self.sub_holes[0].max_x - 2, self.sub_holes[0].max_y,
                                    self.sub_holes[0].max_x - 3,
                                    self.sub_holes[0].max_y - 1, config.ENEMY,
                                    self.sub_holes[0].min_x,
                                    self.sub_holes[0].max_x - 2, self))
        self.enemies.append(
            Enemies(self.holes[1].min_x - 1, self.up_wall.min_y - 1, self.holes[1].min_x - 2,
                    self.up_wall.min_y - 2,
                    config.ENEMY, self.bridges[2].max_x + 1, self.holes[1].min_x - 1, self))
        self.enemies.append(
            Enemies(self.bridges[3].max_x, self.bridges[3].min_y - 1, self.bridges[3].max_x - 1,
                    self.bridges[3].min_y - 2, config.ENEMY, self.bridges[3].min_x,
                    self.bridges[3].max_x, self))

        # Create enemies and bridges on lake
        mid = int((self.lake.min_x + self.lake.max_x) / 2)
        print(self.lake.min_y, self.lake.max_y)
        # print('x_pos -> ', c.LAKES[0].min_x + 5, mid, 10)
        # print('y_pos-> ', c.LAKES[0].min_y - 5, c.TOP - 3, int(c.ROWS / 10))
        # sleep(3)
        min_y = int(config.TOP + self.rows / 10)
        for x_pos, y_pos in zip(range(self.lake.min_x + 5, mid, 10),
                                range(self.lake.min_y - 5, min_y, -int(self.rows / 10))):
            self.bridges.append(Obj(x_pos + 3, y_pos, x_pos - 3, y_pos - 1, config.BRIDGE, self.map_array, self.object_array))
            rand_x = randrange(x_pos - 3, x_pos + 3)
            self.enemies.append(
                Enemies(rand_x + 1, y_pos - 2, rand_x, y_pos - 3, config.ENEMY, x_pos - 3, x_pos + 3, self))
        store = self.bridges[-1]
        self.enemies[-1].kill()
        self.enemies.append(Enemies(store.max_x, store.min_y - 1, store.max_x - 1,
                                      store.min_y - 2, config.ENEMY, store.max_x - 1, store.max_x, self))

        for x_pos, y_pos in zip(range(self.lake.max_x - 5, mid, -10),
                                range(self.lake.min_y - 5, min_y, -int(self.rows / 10))):
            self.bridges.append(Obj(x_pos + 3, y_pos, x_pos - 3, y_pos - 1, config.BRIDGE, self.map_array, self.object_array))
            rand_x = randrange(x_pos - 3, x_pos + 3)
            self.enemies.append(
                Enemies(rand_x + 1, y_pos - 2, rand_x, y_pos - 3, config.ENEMY, x_pos - 3, x_pos + 3, self))
        store_2 = self.bridges[-1]
        self.bridges.append(Obj(store_2.min_x, store.max_y, store.max_x, store.min_y, config.BRIDGE, self.map_array, self.object_array))
        self.enemies[-1].kill()
        self.enemies.append(Enemies(store_2.min_x + 1, store_2.min_y - 1, store_2.min_x,
                                      store_2.min_y - 2, config.ENEMY, store_2.min_x, store_2.min_x + 1, self))
        mid = int((store.max_x + store_2.min_x) / 2)
        self.lives.append(Obj(mid, config.TOP, mid, config.TOP, config.LOVE, self.map_array, self.object_array))

    def create_coins(self):
        # Dependencies: Bridges, walls, holes

        mid = int((self.bridges[0].min_x + self.bridges[0].max_x) / 2)
        self.coins.append(
            Obj(mid, self.bridges[0].min_y - 1, mid, self.bridges[0].min_y - 1, config.COIN, self.map_array, self.object_array))
        mid = int((self.bridges[1].min_x + self.bridges[1].max_x) / 2)

        for x_pos, y_pos in zip(range(mid - 4, mid + 2, 2),
                                range(self.bridges[1].min_y - 1, self.bridges[1].min_y - 4, -1)):
            self.coins.append(Obj(x_pos, y_pos, x_pos, y_pos, config.COIN, self.map_array, self.object_array))
        for x_pos, y_pos in zip(range(mid + 2, mid + 8, 2),
                                range(self.bridges[1].min_y - 2, self.bridges[1].min_y, 1)):
            self.coins.append(Obj(x_pos, y_pos, x_pos, y_pos, config.COIN, self.map_array, self.object_array))

        self.coins.append(Obj(self.sub_holes[0].max_x, self.sub_holes[0].max_y, self.sub_holes[0].max_x, self.sub_holes[0].max_y, config.TIME, self.map_array, self.object_array))
        for x_pos in range(self.holes[0].max_x + 5, self.bridges[2].min_x - 5, 3):
            self.coins.append(Obj(x_pos, self.up_wall.min_y - 1, x_pos, self.up_wall.min_y - 1, config.COIN, self.map_array, self.object_array))

    def create_holes(self):
        # Dependencies: walls, bridges

        rand_x = randrange(int(self.columns / 3), int((2 * self.columns) / 3))
        self.holes.append(Obj(rand_x + 5, self.down_wall.max_y - 2, rand_x, self.up_wall.min_y, ' ', self.map_array, self.object_array))
        self.sub_holes.append(Obj(self.holes[0].max_x + 10, self.holes[0].max_y, self.holes[0].min_x, self.up_wall.min_y + 2, ' ', self.map_array, self.object_array))
        rand_x = randrange(int((4 * self.columns) / 3) + 4, int(5 * self.columns / 3) - 4)
        self.holes.append(Obj(rand_x + 4, self.rows, rand_x - 4, self.up_wall.min_y, ' ', self.map_array, self.object_array))
        self.holes.append(Obj(self.bridges[5].max_x + 24, self.rows, self.bridges[5].max_x + 1, self.up_wall.min_y, ' ', self.map_array, self.object_array))

    def create_extras(self):
        # Dependencies: bridges

        mid = int((self.bridges[1].min_x + self.bridges[1].max_x) / 2)
        self.extras.append(
            Extras(mid + 1, self.bridges[1].max_y, mid - 1, self.bridges[1].min_y,
                   config.EXTRAS_BRIDGE,
                   get_extra(), self.map_array, self.object_array))
        mid = int((self.bridges[3].min_x + self.bridges[3].max_x) / 2)
        self.extras.append(
            Extras(mid + 1, self.bridges[3].max_y, mid - 1, self.bridges[3].min_y,
                   config.EXTRAS_BRIDGE,
                   get_extra(), self.map_array, self.object_array))

    def create_bridges(self):
        # Dependencies: walls

        self.bridges.append(Obj(20, self.up_wall.min_y - 5, 14, self.up_wall.min_y - 7, config.BRIDGE, self.map_array, self.object_array))
        self.bridges.append(Obj(40, self.up_wall.min_y - 5, 25, self.up_wall.min_y - 7, config.BRIDGE, self.map_array, self.object_array))
        self.bridges.append(Obj(self.columns - 4, self.up_wall.min_y - 1, self.columns - 10, self.up_wall.min_y - 7, config.BRIDGE, self.map_array, self.object_array))

        rand_x = randrange(self.columns + 5, int(4 * self.columns / 3) - 5)
        self.bridges.append(Obj(5 + rand_x, self.up_wall.min_y - 5, rand_x - 5, self.up_wall.min_y - 8, config.BRIDGE, self.map_array, self.object_array))

        rand_x = randrange(int(5 * self.columns / 3) + 1, 2 * self.columns - 2)
        self.bridges.append(Obj(rand_x + 1, self.up_wall.min_y - 6, rand_x - 1, self.up_wall.min_y - 8, config.BRIDGE, self.map_array, self.object_array))

        rand_x = randrange(2 * self.columns + 6, int((7 * self.columns) / 3) - 6)
        cross_bridge_list = [[' ' for _ in range(0, 15)] for _ in range(0, 15)]
        for x_pos in range(0, 15):
            for y_pos in range(15 - x_pos, 15):
                cross_bridge_list[x_pos][y_pos] = config.BRIDGE
        self.bridges.append(IrregularObjects({'max_x': rand_x + 6, 'max_y': self.up_wall.min_y - 1, 'min_x': rand_x - 6,'min_y': self.up_wall.min_y - 14}, cross_bridge_list, self.map_array, self.object_array))

    def create_lake_fishes(self):
        # Dependencies: walls

        min_x = int(8 * self.columns / 3)
        max_x = int(11 * self.columns / 3)
        self.lake = Obj(max_x, self.down_wall.max_y - 1, min_x, self.up_wall.max_y, config.WATER, self.map_array, self.object_array)
        rand_x = randrange(self.lake.min_x + 2, self.lake.max_x - 2)
        rand_y = self.lake.min_y + randrange(1, 4)
        self.fishes.append(Obj(rand_x, rand_y, rand_x, rand_y, config.FISH, self.map_array, self.object_array))
        rand_x = randrange(self.lake.min_x + 2, self.lake.max_x - 2)
        rand_y = self.lake.min_y + randrange(1, 4)
        self.fishes.append(Obj(rand_x, rand_y, rand_x, rand_y, config.FISH, self.map_array, self.object_array))

    def create_moving_bridges(self):
        # Dependencies: walls, lake

        min_x = int((11 * self.columns) / 3) + 7
        length = 15
        max_x = int((9 * self.columns) / 2)

        # Create Knifes
        self.thrones.append(Obj(max_x, self.up_wall.max_y + 1, min_x, self.up_wall.max_y, config.THRONES, self.map_array, self.object_array))

        min_y = config.TOP + 5
        max_y = self.lake.min_y - 5
        for x_pos in range(min_x, max_x, 25):
            rand_y = randrange(min_y, max_y + 1)
            self.moving_bridges.append(
                MovingBridges(x_pos + length, rand_y, x_pos, rand_y,
                              config.MOVING_BRIDGES, config.TOP + 5, self.lake.min_y - 5, self))

    def create_walls(self):
        # Dependencies: None

        self.down_wall = Obj(self.length, self.rows, 1, int((9 * self.rows) / 10), config.DOWN_WALL, self.map_array, self.object_array)
        self.up_wall = Obj(self.length, self.down_wall.min_y - 1, 1, self.down_wall.min_y - 1, config.UP_WALL, self.map_array, self.object_array)

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

    def create_pole(self):
        # Dependencies: Walls
        self.pole = Obj(self.length - 5, self.up_wall.min_y - 1, self.length - 5, self.up_wall.min_y - 15, '|', self.map_array, self.object_array)

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
