import curses
import logging

from game.entities.overworld import Overworld
from game.entities.party import Party
from game.settings import settings
from game.states.state import GameState
from game.ui.colors import Colors
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

        # The viewport bounds (into which the game [overworld or scene] is
        # rendered).
        self.viewport = [0, 0, 1, 1]

        # The viewport offset (the y, x offset applied to content rendered
        # within the viewport.
        self.offset = [0, 0]

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

        # Update the viewport to match the screen size
        max_y, max_x = self.game.main_window.getmaxyx()
        self.viewport = [1, 1, max_y - 6, max_x - 1]

        self.game.ui_console.log(
            'terrain',
            self.overworld.get_tile(self.party.y, self.party.x).terrain
        )

        self.game.ui_console.log('position', [self.party.x, self.party.y])

        # @@ TMP: Prevent player getting too far behind
        if self.my_turn:
            self.current_frame_no = self.game.frame_no

        else:

            if self.current_frame_no < (self.game.frame_no - 25):
                self.current_frame_no = self.game.frame_no - 25

            if self.current_frame_no < self.game.frame_no:

                self.last_frame_dt += dt

                if self.last_frame_dt > 0.1:
                    self.current_frame_no += 1

                    if self.current_frame_no in self.game.frames:

                        # @@ TMP
                        last_frame = self.game.frames[self.current_frame_no]
                        if 'data' in last_frame:
                            self.party.x = last_frame['data'][1][0]
                            self.party.y = last_frame['data'][1][1]

        self.offset = self.overworld.get_offset(self.viewport)

    def render(self):
        ctx = self.game.main_window

        # Draw the viewport's content
        self.overworld.render(ctx, self.offset, self.viewport)

        # Draw the viewport border
        t = 0
        l = 0
        b = self.viewport[2] + 1
        r = self.viewport[3] + 1

        border_color = Colors.pair('coyote', settings.ui.bg_color)
        ctx.hline(t, l, curses.ACS_HLINE, r, border_color)
        ctx.hline(b, l, curses.ACS_HLINE, r, border_color)
        ctx.vline(t, l, curses.ACS_VLINE, b, border_color)
        ctx.vline(t, r - 1, curses.ACS_VLINE, b, border_color)

        corner_color = Colors.pair('independence', settings.ui.bg_color)
        ctx.addch(t, l, '┏', corner_color)
        ctx.addch(t, r - 1, '┓', corner_color)
        ctx.addch(b, l, '┗', corner_color)
        ctx.addch(b, r - 1, '┛', corner_color)

        super().render()


# @@ Discuss overworld and scene / entity palettes instead of them being part
#    of the payload
