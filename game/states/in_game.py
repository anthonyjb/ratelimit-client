import curses
import logging

from game.entities.overworld import Overworld
from game.entities.party import Party
from game.settings import settings
from game.states.state import GameState
from game.utils.input import key_pressed


class InGame(GameState):
    """
    The in-game state provides a viewport into the game world, showing either
    the overworld or underworld (a scene) and allowing a player perform
    actions within the game world (such as move north, attack goblin).
    """

    ID = 'in_game'

    def enter(self, **kw):
        super().enter(**kw)

        # The frame number we are currently displaying
        self.current_frame_no = 0

        # Load the game world
        self.overworld = Overworld.from_json_type(
            self.game.client.send('world:read')
        )

        # Load the party
        self.party = Party.from_json_type(self.game.client.send('party:read'))
        self.overworld.party = self.party

        # The time since the last frame update
        self.last_frame_dt = 0

        self.my_turn = False

    def leave(self):
        super().leave()

    def input(self, char):
        super().input(char)

        for i, direction in enumerate(settings.controls.directions.keys()):
            if key_pressed(f'controls.directions.{direction}', char):
                response = self.game.client.send('move', {'direction': i})

                # Immediately move the player as we control them
                if 'position' in response:
                    self.party.x = response['position'][0]
                    self.party.y = response['position'][1]
                    self.my_turn = True

    def update(self, dt):
        super().update(dt)

        self.game.ui_console.log(
            'terrain',
            self.overworld.get_tile(self.party.y, self.party.x).terrain
        )

        self.game.ui_console.log('position', [self.party.x, self.party.y])

        # @@ TMP: Prevent player getting too far behind
        if self.current_frame_no < (self.game.frame_no - 25):
            self.current_frame_no = self.game.frame_no - 25

        if self.current_frame_no < self.game.frame_no and not self.my_turn:

            self.last_frame_dt += dt

            if self.last_frame_dt > 0.1:
                self.current_frame_no += 1

                if self.current_frame_no in self.game.frames:

                    # @@ TMP
                    last_frame = self.game.frames[self.current_frame_no]
                    if 'data' in last_frame:
                        self.party.x = last_frame['data'][1][0]
                        self.party.y = last_frame['data'][1][1]

        self.game.ui_console.log(
            'frame no',
            [self.game.frame_no, self.current_frame_no]
        )

    def render(self):

        self.overworld.render(self.game.main_window)

        super().render()
