from random import sample, randint
from string import ascii_letters
from time import localtime, asctime, sleep

from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

CLIENT = OSCClient('localhost', 3002)


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    while True:
        sleep(1)
        print("running")