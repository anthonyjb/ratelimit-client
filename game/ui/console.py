import curses
import logging
import textwrap

from game.settings import settings
from game.ui.anchor import Anchor
from game.ui.colors import Colors
from game.ui.component import Component
from game.utils.input import key_pressed


# The height of the console
HEIGHT = 6


class Console(Component):
    """
    A UI component for displaying console output.
    """

    def __init__(self):
        super().__init__()

        self.enabled = False
        self.height = 6
        self.right = 0
        self.visible = False
        self.z_index = 1000

        self._buffer = []
        self._offset = 0

    @property
    def can_scroll_down(self):
        return self._offset < len(self._buffer) - self.height

    @property
    def can_scroll_up(self):
        return self._offset > 0

    def clear(self):
        """Clear the console"""
        self._buffer = []

    def log(self, name, value):
        """Log a named value to the console"""
        self._buffer.append((name, value))

    def scroll_down(self):
        """Scroll the console display down"""
        self._offset = min(len(self._buffer) - self.height, self._offset + 1)

    def scroll_up(self):
        """Scroll the console display up"""
        self._offset = max(0, self._offset - 1)

    # Lifecycle methods

    def input(self, char):

        if char == settings.ui.console.toggle_char:

            # Toggle the console
            self.enabled = not self.enabled
            self.visible = self.enabled

        if self.enabled:

            # Support scoll up / down
            if key_pressed('ui.console.scroll_down_char', char):
                self.scroll_down()

            elif key_pressed('ui.console.scroll_up_char', char):
                self.scroll_up()

    def update(self, dt):
        # Update t`he position of the console so that it sticks to the bottom
        # of the window.

        parent_rect = self.parent.rect
        rect = self.rect
        self.top = parent_rect[2] - self.height

        super().update(dt)

    def render(self, ctx):

        if not self.visible:
            return

        t, l, h, w = self.rect
        b = t + h - 1
        r = l + w - 1

        win = ctx.subwin(t, 0)

        # Clear console area
        win.bkgd(
            ' ',
            Colors.pair(
                settings.ui.console.fg_color,
                settings.ui.console.bg_color
            )
        )
        win.erase()

        # Display the buffer
        for i, pair in enumerate(self._buffer[-self.height:]):
            win.insstr(i, 0, f'{pair[0]}: {pair[1]}')

        super().render(ctx)


# @@
#
# - support scrolling
# - handle line return
# - handle maps larger than scroll in the window
#
