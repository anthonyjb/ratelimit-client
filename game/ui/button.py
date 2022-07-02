import curses
import textwrap

from game.settings import settings
from game.ui.component import Component
from game.ui.event import Event
from game.utils.colors import Colors


class Button(Component):
    """
    A button which can be selected by pressing a key.

    If you specify any as the key then any key will trigger the button to be
    selected.
    """

    def __init__(self, label, key, color_pair=None):
        super().__init__()

        self.height = 1
        self.key = key.lower()
        self.color_pair = color_pair or Colors.pair(
            settings.ui.primary_button_color,
            settings.ui.bg_color
        )

        self.label = label

    @property
    def full_label(self):
        return f' [ {self.label} <{self.key.upper()}> ] '

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.width = len(self.full_label)

    def input(self, char):

        if char:
            if chr(char) == self.key:
                self.dispatch_event(Event('select'))

            if self.key == 'any':
                self.dispatch_event(Event('select'))

    def render(self, ctx):

        t, l, h, w = self.rect

        ctx.addstr(
            t,
            l + 1,
            self.full_label,
            self.color_pair | curses.A_BOLD
        )
