import curses
import logging

from game.entities.overworld import Overworld
from game.entities.party import Party
from game.settings import settings
from game.states.state import GameState
from game.utils.colors import Colors
from game.utils.input import key_pressed
from game.utils.rendering import Viewport
from game.utils.sprites import SpriteSheet


class InGame(GameState):
    """
    The in-game state provides a viewport into the game world, showing either
    the overworld or underworld (a scene) and allowing a player perform
    actions within the game world (such as move north, attack goblin).
    """

    ID = 'in_game'

    def enter(self, **kw):
        super().enter(**kw)

    def leave(self):
        super().leave()

    def input(self, char):
        super().input(char)

    def update(self, dt):
        super().update(dt)

        if self.paused:
            return

        self.game_state_manager.push('overworld')


# @@
#
# - Move sprite sheet load to game loop start code
# - Go back to rendering the overworld, update it to use the new spritesheet
#   and json type data.
#
