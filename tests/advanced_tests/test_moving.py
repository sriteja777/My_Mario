import sys
sys.path.append('/home/sriteja/PycharmProjects/My_Mario/mymario')


import old_game
from motion import Player

up_wall, down_wall = old_game.create_level1_map()
old_game.c.PLAYER_OBJ.append(
    Player({'max_x': 4, 'max_y': up_wall.min_y - 1, 'min_x': 3, 'min_y': up_wall.min_y - 2},
           old_game.c.PLAYER)
)


def test_move_left():
    temp = old_game.c.PLAYER_OBJ[0].min_x
    old_game.c.PLAYER_OBJ[0].move_left()
    assert old_game.c.PLAYER_OBJ[0].min_x == temp - 1


def test_move_right():
    temp = old_game.c.PLAYER_OBJ[0].min_x
    old_game.c.PLAYER_OBJ[0].move_right()
    assert old_game.c.PLAYER_OBJ[0].min_x == temp + 1


def test_move_up():
    temp = old_game.c.PLAYER_OBJ[0].min_y
    old_game.c.PLAYER_OBJ[0].move_up(down=False, dist=1)
    assert old_game.c.PLAYER_OBJ[0].min_y == temp - 1
    old_game.c.PLAYER_OBJ[0].move_down()


def test_moving_down():
    temp = old_game.c.PLAYER_OBJ[0].min_y
    old_game.c.PLAYER_OBJ[0].move_down()
    assert old_game.c.PLAYER_OBJ[0].min_y == temp
