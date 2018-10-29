import sys
sys.path.append('/home/sriteja/PycharmProjects/My_Mario/mymario')

import motion as m
import config as c
enemy = m.Enemies(4, 5,  6, 7, c.ENEMY, 10, 20)


def test_init():
    assert enemy.max_y == 5