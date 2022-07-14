import curses
import logging

from game import entities
from game.settings import settings
from game.states.state import GameState
from game.utils.colors import Colors
from game.utils.input import key_pressed
from game.utils.rendering import Viewport


class Overworld(GameState):
    """
    A view of the game overworld which the party can navigate around. The
    overworld state should only be entered from the in-game state.
    """

    ID = 'overworld'

    def enter(self, **kw):
        super().enter(**kw)

        self.overworld = None
        self.party = None

        # A viewport to render the game world within
        self.viewport = Viewport()

        # Bootstraps
        self.game.bootstrap(
            'Fetching overworld...',
            lambda: self.fetch_overworld()
        )

    def input(self, char):
        super().input(char)

        if key_pressed(f'controls.enter_scene', char):
            response = self.game.client.send('party:enter_scene')
            if response['success']:
                self.game_state_manager.pop(in_scene=True)

    def update(self, dt):
        super().update(dt)

        if self.paused:
            return

    def render(self):

        if self.paused:
            return

        ctx = self.game.main_window

        max_y, max_x = self.game.main_window.getmaxyx()

        # Clear dynamic layer for viewport
        self.viewport.clear(z=1)

        # Render the dynamic elements within the overworld
        self.overworld.render(self.viewport)

        # Draw the viewport's content
        viewport_rect = [2, 1, max_y - 9, max_x - 3]

        self.viewport.render(
            ctx,
            viewport_rect[0:2],
            viewport_rect[2:],
            self.overworld.get_offset([max_y - 8, max_x - 4])
        )

        # Draw the viewport border
        t = 1
        l = 0
        b = viewport_rect[2] + 3
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

    # Bootstraps

    def fetch_overworld(self):
        """Fetch the overworld from the server"""
        self.overworld = entities.overworld.Overworld.from_json_type(
            self.game.client.send('world:read')
        )

        self.party = entities.party.Party.from_json_type(
            self.game.client.send('party:read')
        )

        self.overworld.party = self.party

        # Render static elements within the overworld to the viewport
        self.overworld.render_static(self.viewport)
