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

        self.sprite_sheet = SpriteSheet.from_json_type(
            self.game.client.send('sprite_sheet:read')
        )

    def leave(self):
        super().leave()

    def input(self, char):
        super().input(char)

    def update(self, dt):
        super().update(dt)

    def render(self):
        ctx = self.game.main_window

        self.game.ui_console.log(
            'sprite',
            self.sprite_sheet.get('biomes', (4,))
        )

# @@
#
# - Move sprite sheet load to game loop start code
#
