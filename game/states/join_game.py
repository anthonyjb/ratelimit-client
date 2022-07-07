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

        self.response = None

        """

        so when you boot strap something the calling code wont stop because
        bootstrap runs one update and render before executing the task.
        So on that basis we have to have a think about what we're doing below,
        either force clear / render UI and make bootstrap simply block until
        its done (e.g don't really need a state).

        the other problem with bootstrapping currently is that if there are
        two called in a row the last one will get called first because it's a
        stack that goes on.

        - could this be solved by insisting that push / collapse is only ever
          called in update (think we'd need a ready flag)

        - another option is perhaps to have bootstrap call the next state, e.g
          send it 'next_state', 'next_state_args', 'collapse/pop'. think this
          is the solution

        """

        # self.game.bootstrap(
        #     'Attempting to join game...',
        #     lambda: self.join()
        # )

        self.join()

        # joined = self.response['joined']
        # reason = self.response.get('reason')

        # if joined:
        #     state.game_state_manager.collapse('in_game')

        # else:

        #     if reason == 'player_not_registered':
        #         state.game_state_manager.collapse('create_character')

        #     elif reason == 'party_not_in_overworld':

        #         while not joined:

        #             self.game.bootstrap(
        #                 'Waiting for party to return to overworld...',
        #                 lambda: self.join()
        #             )
        #             joined = self.response['joined']

        #             if not joined:
        #                 time.sleep(5)

        #         state.game_state_manager.collapse('in_game')

    # Bootstraps

    def join(self):
        """Attempt to join the game on the server"""
        self.response = self.game.client.send('game:join')


# @@ Maybe store player details against the game, or have a strucure to make
#    it simple to have data that persists between scenes.

#
# {
#     "joined": false,
#     "reason": "player_not_registered|party_not_in_overworld",
# } (
#
