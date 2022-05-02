import curses
import textwrap

from game.settings import settings
from game.ui.colors import Colors
from game.ui.component import Component


class Button(Component):
    """
    A button which can be selected by pressing a key.
    """

    def __init__(self, label, key, color_pair=None):
        super().__init__()

        self.label = label
        self.key = key
        self.color_pair = color_pair or Colors.pair(
            settings.ui.bg_color,
            settings.ui.fg_color
        )

    def render(self, ctx):

        t, r, b, l = self.rel_extents

        ctx.addstr(t, l, f'[ {self.label} - ({self.key}) ]', self.color_pair)
