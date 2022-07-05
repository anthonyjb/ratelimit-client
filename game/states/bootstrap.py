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


class Bootstrap(GameState):
    """
    The bootstrap scene is designed to perform a given task and display a
    message while doing so before removing itself from the stack. For example
    loading a sprite
    """

    ID = 'bootstrap'

    def enter(self, message, task, **kw):
        super().enter(**kw)

        self._message = message
        self._task = task
        self._ready = False

    def update(self, dt):
        super().update(dt)

        if self._ready:
            self._task()
            self.game_state_manager.pop()

        else:
            self._ready = True

    def render(self):

        self.game.main_window.addstr(1, 1, self._message)
