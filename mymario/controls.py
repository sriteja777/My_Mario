

class ObjectSetup(object):
    pass


def set_keys_for_player(up=None, left=None, right=None, up_right=None, up_left=None, bullet=''):
    keys = ObjectSetup()
    keys.UP = up
    keys.LEFT = left
    keys.RIGHT = right
    keys.UP_RIGHT = up_right
    keys.UP_LEFT = up_left
    keys.BULLET = bullet
    return keys


class Controls:
    def __init__(self):
        self.player = []
        self.player.append(set_keys_for_player('w', 'a', 'd', 'e', 'z', 's'))
        self.player.append(set_keys_for_player('w', 'a', 'd', 'e', 'z', 's'))
        # self.player.append(set_keys_for_player('t', 'f', 'h', 'y', 'v', 'g'))
        self.player.append(set_keys_for_player('i', 'j', 'l', 'o', 'm', 'k'))
        self.player.append(set_keys_for_player('8', '4', '6', '9', '1', '5'))
