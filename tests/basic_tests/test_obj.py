import sys
sys.path.append('/home/sriteja/PycharmProjects/My_Mario/mymario')

import objects as o
import config as c
ob = o.Obj(10, 10, 5,6, 'a')


def test_init():
    assert (ob.max_x, ob.max_y, ob.min_x, ob.min_y, ob.string, ob.check_ends) == (10, 10, 5, 6, 'a', False)


def test_update():
    ob.min_x = 4
    ob.min_y = 5
    ob.max_y = 9
    ob.max_x = 9
    ob.update()
    assert c.DIMENSIONAL_ARRAY[8][3] == 'a'

def test_remove():
    ob.min_x = 4
    ob.min_y = 5
    ob.max_y = 9
    ob.max_x = 9
    ob.update()
    ob.remove()
    assert c.DIMENSIONAL_ARRAY[8][3] == ' '