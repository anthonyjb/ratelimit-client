import curses
import textwrap

from game.ui.anchor import Anchor
from game.ui.component import Component


class InfoPanel(Component):
    """
    A UI component that displays panel of information.
    """

    def __init__(self, title, body):
        super().__init__()

        self.title = title
        self.body = body

        self.buttons = Anchor(Anchor.BOTTOM | Anchor.RIGHT, (0, 4))
        self.add_child(self.buttons)

    def update(self, dt):
        # Upate the position and size of the panel based on the width of the
        # panel and the body text.

        parent_height = self.parent.rect[2]

        t, l, h, w = self.rect
        rows = len(textwrap.wrap(self.body, w - 5))

        self.top = round((parent_height - (rows + 4)) / 2)
        self.height = rows + 4

        super().update(dt)

    def render(self, ctx):

        ctx.clear()

        if not self.visible:
            return

        t, l, h, w = self.rect
        b = t + h - 1
        r = l + w - 1

        # Draw the border
        ctx.hline(t, l, curses.ACS_HLINE, w)
        ctx.hline(b, l, curses.ACS_HLINE, w)
        ctx.vline(t, l, curses.ACS_VLINE, h)
        ctx.vline(t, r, curses.ACS_VLINE, h)

        ctx.addch(t, l, curses.ACS_ULCORNER)
        ctx.addch(t, r, curses.ACS_URCORNER)
        ctx.addch(b, l, curses.ACS_LLCORNER)
        ctx.addch(b, r, curses.ACS_LRCORNER)

        # Draw the title
        title = f' {self.title[:w - 3]} '
        ctx.addstr(
            t,
            l + round((w + 1 - len(title)) / 2),
            title,
            curses.A_BOLD
        )

        # Draw the body
        body = textwrap.fill(self.body, w - 5)
        body_box = ctx.derwin(h, w - 4, t + 2, l + 3)
        body_box.addstr(0, 0, body)

        super().render(ctx)

