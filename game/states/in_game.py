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

    def update(self, dt):
        super().update(dt)

    def render(self):

        self.overworld.render(self.game.main_window)

        super().render()


# Overworld
#
# - size (w, h)
# - terrains [strings, woods, plain, hills, mountains, mountain peaks desert, water]
# - landmarks [string, settlement, cave]
# - tiles []
#     - terrain index
#     - landmark index

# {
#     'landmarks': ['cave', 'settlement'],
#     'size': [40, 20],
#     'terrains': ['hills', 'moutain peaks', 'mountains', 'plains', 'water', 'woods'],
#     'tiles': [[5, -1], [3, -1], [3, 1], ...]
# }
