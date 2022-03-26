"""
A console based 'RateLimit' game client.
"""

from game.loop import GameLoop


if __name__ == '__main__':

    loop = GameLoop()
    loop.init()
    loop.run()
