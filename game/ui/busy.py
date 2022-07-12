import curses

from game.settings import settings
from game.ui.anchor import Anchor
from game.ui.component import Component
from game.utils.colors import Colors


class Busy(Component):
    """
    A UI component that displays a single message while the client is busy.
    """

    def __init__(self):
        super().__init__()

        self.message = ''

        self.bottom = 0
        self.right = 0
        self.visible = False
        self.z_index = 999

    def render(self, ctx):

        if not self.visible:
            return

        win = ctx.subwin(0, 0)
        win.bkgd(' ', Colors.pair(settings.ui.fg_color, settings.ui.bg_color))
        win.erase()
        win.addstr(1, 1, self.message)
