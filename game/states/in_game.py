import curses
import logging

from game.entities.overworld import Overworld
from game.states.state import GameState


class InGame(GameState):
    """
    The in-game state provides a viewport into the game world, showing either
    the overworld or underworld (a scene) and allowing a player perform
    actions within the game world (such as move north, attack goblin).
    """

    ID = 'in_game'

    def enter(self, **kw):
        super().enter(**kw)

        # Load the game world
        self.overworld = Overworld.from_json_type(
            self.game.client.send('view_world')
        )

    def leave(self):
        super().leave()

    def input(self, char):
        super().input(char)

        # TMP
        if char == 259:
            self.game.client.send('move', {'direction': 1})

    def update(self, dt):
        super().update(dt)

    def render(self):

        self.overworld.render(self.game.main_window)

        super().render()
