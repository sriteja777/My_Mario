import os
import time

up = '\x1b[{}A'
down = '\x1b[{}B'
right = '\x1b[{}C'
left = '\x1b[{}D'

print("Hello" + left.format(3), end='', flush=True)
time.sleep(2)
print("W", end='', flush=True)
time.sleep(4)
