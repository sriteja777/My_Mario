import sys
sys.path.append('/home/sriteja/PycharmProjects/My_Mario/mymario')


import game
from motion import Player

up_wall, down_wall = game.create_level1_map()
game.c.PLAYER_OBJ.append(
    Player({'max_x': 4, 'max_y': up_wall.min_y - 1, 'min_x': 3, 'min_y': up_wall.min_y - 2},
           game.c.PLAYER)
)


def test_move_left():
    temp = game.c.PLAYER_OBJ[0].min_x
    game.c.PLAYER_OBJ[0].move_left()
    assert game.c.PLAYER_OBJ[0].min_x == temp - 1


def test_move_right():
    temp = game.c.PLAYER_OBJ[0].min_x
    game.c.PLAYER_OBJ[0].move_right()
    assert game.c.PLAYER_OBJ[0].min_x == temp + 1


def test_move_up():
    temp = game.c.PLAYER_OBJ[0].min_y
    game.c.PLAYER_OBJ[0].move_up(down=False, dist=1)
    assert game.c.PLAYER_OBJ[0].min_y == temp - 1
    game.c.PLAYER_OBJ[0].move_down()


def test_moving_down():
    temp = game.c.PLAYER_OBJ[0].min_y
    game.c.PLAYER_OBJ[0].move_down()
    assert game.c.PLAYER_OBJ[0].min_y == temp
