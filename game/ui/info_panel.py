import curses
import textwrap

from game.ui.component import Component


class InfoPanel(Component):
    """
    A UI component that displays pannel of information.
    """

    def __init__(self, title, body):
        super().__init__()

        self.title = title
        self.body = body

        from game.ui.button import Button

        self.button = Button('Test', 't')
        self.add_child(self.button)

    def update(self, dt):

        # Upate the position and size of the panel based on the width of the
        # panel and the body text.

        t, r, b, l = self.rel_extents
        rows = len(textwrap.wrap(self.body, r - l - 5))

        self.top = round((self.parent.height - (rows + 4)) / 2)
        self.height = rows + 4

        self.button.top = self.height - 1

        super().update(dt)

    def render(self, ctx):

        if not self.visible:
            return

        t, r, b, l = self.rel_extents
        b -= 1
        h = b - t
        w = r - l

        # Draw the border
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


# - Finish anchor class
# - Create a buttons anchor component aligned BOTTOM (CENTER)
# - Add buttons to the anchor component infor_pannel.buttons.add_child()
# - Change the size of the anchor class to accommodate the buttons for the
#   info panel on update.
#   - Create layout helper to allow me to layout all the buttons horizonally
#     with a gap between each `layout(components, direction, gap)`.
# - Finish support for buttons
#
# Button(label, key, color_pair, handler)
# - https://stackoverflow.com/questions/39267464/advanced-mailto-use-in-python
#   for initializing the email send for the error if they agree
