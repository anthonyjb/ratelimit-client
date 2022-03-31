"""
A console based 'RateLimit' game client.
"""

import asyncio

from game.loop import GameLoop


if __name__ == '__main__':

    loop = GameLoop()
    loop.init()
    asyncio.run(loop.run())
