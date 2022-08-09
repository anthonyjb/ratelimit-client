import curses

from game.settings import settings
from game.ui.component import Component
from game.utils.colors import Colors


class Border(Component):
    """
    A component that will display a stylized border.
    """

    def render(self, ctx):

        if not self.visible:
            return

        t, l, h, w = self.rect
        b = t + h - 1
        r = l + w - 1

        # Draw the viewport border
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
