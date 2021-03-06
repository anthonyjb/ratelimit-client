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

        self.in_scene = kw.get('in_scene', False)
        if self.in_scene:
            self.active_player = kw['active_player']

    def resume(self, **kw):
        super().resume(**kw)

        self.in_scene = kw.get('in_scene', False)
        if self.in_scene:
            self.active_player = kw['active_player']

    def leave(self):
        super().leave()

    def input(self, char):
        super().input(char)

    def update(self, dt):
        super().update(dt)

        if self.paused:
            return

        if self.in_scene:
            self.game_state_manager.push(
                'scene',
                active_player=self.active_player
            )

        else:
            self.game_state_manager.push('overworld')

