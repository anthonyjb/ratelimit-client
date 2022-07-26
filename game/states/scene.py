import curses
import logging

from game import entities
from game.settings import settings
from game.states.state import GameState
from game.utils.colors import Colors
from game.utils.rendering import Viewport


class Scene(GameState):
    """
    A view of the a scene (e.g a dungeon, village, woodland) within the game
    the party has entered. The scene state should only be entered from the
    in-game state.
    """

    ID = 'scene'

    def enter(self, **kw):
        super().enter(**kw)

        self.scene = None
        self.player = None

        # A viewport to render the game world within
        self.viewport = Viewport()

        # Bootstraps
        self.game.bootstrap(
            'Fetching scene...',
            lambda: self.fetch_scene()
        )

    def render(self):

        if self.paused:
            return

        ctx = self.game.main_window

        max_y, max_x = self.game.main_window.getmaxyx()

        # Clear the viewport
        self.viewport.clear()

        # Render the dynamic elements within the overworld
        self.scene.render(self.viewport)

        # Draw the viewport's content
        viewport_rect = [2, 1, max_y - 9, max_x - 3]

        self.viewport.render(
            ctx,
            viewport_rect[0:2],
            viewport_rect[2:],
            self.scene.get_offset(self.player.yx, [max_y - 8, max_x - 4])
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

    def fetch_scene(self):
        """Fetch the scene from the server"""
        self.scene = entities.scene.Scene.from_json_type(
            self.game.client.send('scene:read')
        )

        # @@ TODO: Fetch from server
        self.player = entities.player.Player()

# @@ Create a UI component for the viewport border as this code is
# reported.
