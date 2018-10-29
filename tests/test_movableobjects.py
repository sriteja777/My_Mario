import sys
sys.path.append('/home/sriteja/PycharmProjects/My_Mario/mymario')

from objects import MovableObjects


class SampleMovableObjects(MovableObjects):
    def __init__(self):
        MovableObjects.__init__(self, 4, 4, 3, 3, 'a')

    def clash(self, clashed_with, object_clashed):
        pass

    def wrong_move(self):
        pass

def test_init():
    mov_ob = SampleMovableObjects()
    assert mov_ob.is_alive

# mov_ob = MovableObjects(10, 10, 5, 6, 'a')
#
#
# def test_init():
#     assert mov_ob.is_alive
