import curses
import logging

from game import entities
from game.settings import settings
from game.states.state import GameState
from game.utils.colors import Colors
from game.utils.input import key_pressed
from game.utils.rendering import Viewport


class Scene(GameState):
    """
    A view of the a scene (e.g a dungeon, village, woodland) within the game
    the party has entered. The scene state should only be entered from the
    in-game state.
    """

    ID = 'scene'

    def enter(self, **kw):
        super().enter(**kw)

        # A viewport to render the game world within
        self.viewport = Viewport()

    def render(self):

        if self.paused:
            return

        ctx = self.game.main_window

        ctx.addstr(1, 1, 'In-scene')

        super().render()
