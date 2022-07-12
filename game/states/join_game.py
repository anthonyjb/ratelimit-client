import curses
import time

from game.entities.overworld import Overworld
from game.entities.party import Party
from game.settings import settings
from game.states.state import GameState
from game.utils.colors import Colors
from game.utils.input import key_pressed
from game.utils.rendering import Viewport
from game.utils.sprites import SpriteSheet


class JoinGame(GameState):
    """
    Attempt to join the game.
    """

    ID = 'join_game'

    def enter(self, **kw):
        super().enter(**kw)

        self._status_message = 'Attempting to join game...'

        self._waited = None

    def update(self, dt):
        super().update(dt)

        if self.paused:
            return

        if self.slept(1):

            joined, reason = self.game.bootstrap(
                self._status_message,
                lambda: self.join()
            )

            if joined:
                self.game_state_manager.collapse('in_game')

            if reason == 'player_not_registered':
                self.game_state_manager.collapse('create_character')

            elif reason == 'party_not_in_overworld':
                self._status_message \
                        = 'Waiting for party to return to overworld...'

    # Bootstraps

    def join(self):
        """Attempt to join the game on the server"""
        response = self.game.client.send('game:join')
        return (response['joined'], response.get('reason', ''))
