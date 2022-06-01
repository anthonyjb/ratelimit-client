import curses
import logging
import textwrap

from game.ui.anchor import Anchor
from game.ui.component import Component


# The height of the console
HEIGHT = 6


class Console(Component):
    """
    A UI component for displaying console output.
    """

    def __init__(self):
        super().__init__()

        self.right = 0
        self.height = 6
        self.visible = False
        self.z_index = 1000

        self._buffer = []

    def clear(self):
        """Clear the console"""
        self._buffer = []

    def log(self, name, value):
        """Log a named value to the console"""
        self._buffer.append((name, value))

    def update(self, dt):
        # Update the position of the console so that it sticks to the bottom
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

        # Clear console area
        ctx.move(t, l)
        ctx.clrtobot()

        # Draw the border
        ctx.hline(t - 1, l, curses.ACS_HLINE, w)

        # Display the buffer
        for i, pair in enumerate(self._buffer[-self.height:]):
            ctx.insstr(t + i, 0, f'{pair[0]}: {pair[1]}')

        super().render(ctx)
