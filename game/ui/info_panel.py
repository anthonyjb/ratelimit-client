import curses
import logging

from game.ui.component import Component


class InfoPanel(Component):
    """
    A UI component that displays pannel of information.
    """

    def render(self, ctx):

        # Draw ctx
        t, r, b, l = self.rel_extents
        w = r - l - 1
        h = b - t - 1

        ctx.hline(t, l, curses.ACS_HLINE, w)
        ctx.hline(b - 1, l, curses.ACS_HLINE, w)
        ctx.vline(t, l, curses.ACS_VLINE, h)
        ctx.vline(t, r - 1, curses.ACS_VLINE, h)
        ctx.addch(t, l, curses.ACS_ULCORNER)
        ctx.addch(t, r - 1, curses.ACS_URCORNER)
        ctx.addch(b - 1, l, curses.ACS_LLCORNER)
        ctx.addch(b - 1, r - 1, curses.ACS_LRCORNER)
        ctx.refresh()

        super().render(ctx)


# @@
#
# - Investigate weird bottom-right character can't be rendered without error?
# - Display title
# - Display message
# - Tabbed items in UI to support for tabbing between buttons?
#
