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


class CreateCharacter(GameState):
    """
    Allow the player to create their character.
    """

    ID = 'create_character'

    def enter(self, **kw):
        super().enter(**kw)

    def render(self):

        self.game.main_window.addstr(1, 1, 'CREATE CHARACTER')


# ?? Add current state as a default to the console
