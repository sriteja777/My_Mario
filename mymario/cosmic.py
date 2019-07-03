import threading

changes_lock = threading.Lock()
changes = []
pointer = 0
f = open('temp', 'a')


def register_changes(i, j, string):
    f = open('temp', 'a')
    changes_lock.acquire()
    change = {'x': j, 'y': i, 'string': string}
    changes.append(change)
    changes_lock.release()
    f.write(str(change) + '\n')


def print_changes():
    for change in changes:
        print(str(change))