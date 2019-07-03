
class Cursor:
    def __init__(self):
        self.esc = '\x1b['
        self._up = '\x1b[{}A'
        self._down = '\x1b[{}B'
        self._right = '\x1b[{}C'
        self._left = '\x1b[{}D'
        self._position = '\x1b[{1};{0}H'
        pass

    def left(self, x=1):
        print(self._left.format(x))

    def right(self, x=1):
        print(self._right.format(x))

    def up(self, x=1):
        print(self._up.format(x))

    def down(self, x=1):
        print(self._down.format(x))

    def top(self):
        print(self._position.format(1, 1), end='', flush=True)

    def position(self, x, y):
        print(self._position.format(x, y), end='', flush=True)

    def put_char(self, x, y, ch):
        self.position(x, y)
        print(str(ch), end='', flush=True)