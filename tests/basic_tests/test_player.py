# from path import mymario as m
import sys
sys.path.append('/home/sriteja/PycharmProjects/My_Mario/mymario')
# sys.path.insert(0, '../mymario/')
import motion as m
import config as c
import game as g

player = m.Player({'max_x': 4, 'max_y': 5, 'min_x':  6, 'min_y': 7}, c.PLAYER)


def test_init():
    assert (player.min_x, player.max_y, player.string, player.time) == (6, 5, c.PLAYER, c.DEFAULT_TIMEOUT)


def test_get_lives():
    assert player.get_lives() == c.DEFAULT_LIVES


def test_update_live():
    store = player.get_lives()
    player.update_live(1)
    assert player.get_lives() == store + 1
