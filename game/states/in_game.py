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

    def leave(self):
        super().leave()

    def input(self, char):
        super().input(char)

        for i, direction in enumerate(settings.controls.directions.keys()):
            if key_pressed(f'controls.directions.{direction}', char):
                self.game.client.send('move', {'direction': i})

    def update(self, dt):
        super().update(dt)

        if self.current_frame_no < self.game.frame_no:
            self.current_frame_no = self.game.frame_no

            # @@ TMP
            last_frame = self.game.frames[self.game.frame_no]
            if 'data' in last_frame:
                self.party.x = last_frame['data'][1][0]
                self.party.y = last_frame['data'][1][1]

        self.game.ui_console.log(
            'frame no',
            [self.game.frame_no, self.current_frame_no]
        )

        # predictive movement

    def render(self):

        self.overworld.render(self.game.main_window)

        super().render()
