import curses
import logging

from game.entities.overworld import Overworld
from game.entities.party import Party
from game.settings import settings
from game.states.state import GameState
from game.ui.colors import Colors
from game.utils.input import key_pressed
from game.utils.rendering import Viewport


class InGame(GameState):
    """
    The in-game state provides a viewport into the game world, showing either
    the overworld or underworld (a scene) and allowing a player perform
    actions within the game world (such as move north, attack goblin).
    """

    ID = 'in_game'

    def enter(self, **kw):
        super().enter(**kw)

        # A viewport to render the game world within
        self.viewport = Viewport()

        # The frame number we are currently displaying
        self.current_frame_no = -1

        # Load the game world
        self.overworld = Overworld.from_json_type(
            self.game.client.send('world:read')
        )

        # Load the party
        self.party = Party.from_json_type(self.game.client.send('party:read'))
        self.overworld.party = self.party

        # Render static elements within the overworld to the viewport
        self.overworld.render_static(self.viewport)

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

        # @@ TMP: Prevent player getting too far behind
        if self.my_turn:
            self.current_frame_no = self.game.frame_no

        else:

            if (
                self.current_frame_no == -1
                and self.current_frame_no < self.game.frame_no
            ):
                self.current_frame_no = self.game.frame_no

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

    def render(self):
        ctx = self.game.main_window

        max_y, max_x = self.game.main_window.getmaxyx()

        # Clear dynamic layer for viewport
        self.viewport.clear(1)

        # Render the dynamic elements within the overworld
        self.overworld.render(self.viewport)

        # Draw the viewport's content
        viewport_rect = [1, 1, max_y - 9, max_x - 3]

        self.viewport.render(
            ctx,
            viewport_rect[0:2],
            viewport_rect[2:],
            self.overworld.get_offset([max_y - 8, max_x - 4])
        )

        # Draw the viewport border
        t = 0
        l = 0
        b = viewport_rect[2] + 2
        r = viewport_rect[3] + 2

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

        self.game.ui_console.log(
            'terrain',
            self.overworld.get_tile(self.party.y, self.party.x).terrain
        )

        self.game.ui_console.log(
            'offset',
            self.overworld.get_offset([max_y - 8, max_x - 4])
        )

# @@ Discuss overworld and scene / entity palettes instead of them being part
#    of the payload
