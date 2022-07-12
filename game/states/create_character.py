import curses
import logging
import time

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

    def update(self, dt):

        created, payload = self.game.bootstrap(
            'Attempting to create a game...',
            lambda: self.create_character()
        )

        if created:
            self.game_state_manager.collapse('join_game')

        else:
            time.sleep(10)

    # Bootstraps

    def create_character(self):
        """Attempt to create a character for the player"""
        response = self.game.client.send(
            'player:create',
            {
                'name': 'Ant',
                'race': 'dwarf',
                'profession': 'mage'
            }
        )

        if response['success']:
            return True, response['player']

        return False, response['reason']

# ?? Add current state as a default to the console
