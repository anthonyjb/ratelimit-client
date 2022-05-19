import curses
import logging

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

        # world = self.game.client.send('view_world')

        # logging.info(world)

    def leave(self):
        super().leave()

    def input(self, char):
        super().input(char)

    def update(self, dt):
        super().update(dt)

    def render(self):

        self.game.main_window.addstr(1, 1, 'In-game state', curses.A_BOLD)

        super().render()
