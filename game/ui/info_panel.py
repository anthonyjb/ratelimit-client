import curses
import logging

from game.ui.component import Component


class InfoPanel(Component):
    """
    A UI component that displays pannel of information.
    """

    def __init__(self, title):
        super().__init__()
        self.title = title

    def render(self, ctx):

        # Draw the border
        t, r, b, l = self.rel_extents
        b -= 1
        w = r - l
        h = b - t

        ctx.hline(t, l, curses.ACS_HLINE, w)
        ctx.hline(b, l, curses.ACS_HLINE, w)
        ctx.vline(t, l, curses.ACS_VLINE, h)
        ctx.vline(t, r, curses.ACS_VLINE, h)
        ctx.addch(t, l, curses.ACS_ULCORNER)
        ctx.addch(t, r, curses.ACS_URCORNER)
        ctx.addch(b, l, curses.ACS_LLCORNER)

        # Insert else the cursor position could be moved out of position
        ctx.insch(b, r, curses.ACS_LRCORNER)

        # Draw the title
        title = self.title[:w - 2]
        title = f' {title} '
        title_left = l + ((w - len(title)) // 2)

        if curses.can_change_color():
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)

        ctx.bkgd(' ', curses.color_pair(1) | curses.A_BOLD)
        ctx.addstr(t, title_left, title)

        ctx.refresh()

        super().render(ctx)


# @@
#
# - Display title
# - Display message
# - Tabbed items in UI to support for tabbing between buttons?
#
