class ObjectSetup(object):
    pass


def set_keys_for_player(up='', left='', right='', up_right='', up_left=''):
    keys = ObjectSetup()
    keys.UP = up
    keys.LEFT = left
    keys.RIGHT = right
    keys.UP_RIGHT = up_right
    keys.UP_LEFT = up_left
    return keys


class Controls:
    def __init__(self):
        self.player = []
        self.player.append(set_keys_for_player('w', 'a', 'd', 'e', 'z'))
        self.player.append(set_keys_for_player('i', 'j', 'l', 'o', 'm'))
