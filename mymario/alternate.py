import os
from time import sleep

print("\033[?1049h\033[H")
print("Alternate buffer!")

for i in range(5, 0, -1):
    print("Going back in:", i)
    # sleep(1)

print("Hello\n" *10)
sleep(5)
os.system('clear')
print("World \n" * 9)
sleep(5)
print("\033[?1049l")

