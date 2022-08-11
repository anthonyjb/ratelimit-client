import curses

from game.settings import settings
from game.ui.component import Component
from game.utils.colors import Colors


class StatBar(Component):
    """
    A UI component typically displayed under the viewport displaying the party
    or players various stats. The stat bar can span multiple lines depending
    on the number of stats and available screen width.
    """

    def __init__(self, gap=4):
        super().__init__()

        self.gap = gap

    def update(self, dt):
        super().update(dt)

        left = 0
        for child in self.children:
            child.left = left
            left += child.width + self.gap

    def render(self, ctx):
        super().render(ctx)


class Stat(Component):
    """
    A stat displayed within a stat bar. Stats support a number of formats:

    - value [value only]
    - label: value [label and value]
    - label: value * [label and two values where the second value is a boolean]
    - label: value (value) [label and two values]

    """

    def __init__(self, value, label=None, color=None):
        super().__init__()

        self.value = value
        self.label = label
        self.color = color

    @property
    def width(self):
        w = 0

        label = self.label
        value = self.value

        if label:
            w += len(label) + 2

        if isinstance(value, (list, tuple)):
            if isinstance(value[1], bool):
                if value[1]:
                    w += len(str(value[0])) + 1
                else:
                    w += len(str(value[0]))
            else:
                w += len(str(value[0])) + len(str(value[1])) + 3
        else:
            w += len(str(value))

        return w

    @width.setter
    def width(self, value):
        pass

    def render(self, ctx):
        t, l, h, w = self.rect

        label = self.label
        value = self.value

        color = Colors.pair(
            self.color or settings.ui.fg_color,
            settings.ui.bg_color
        )

        if label:
            ctx.addstr(t, l, f'{label}:', color | curses.A_BOLD)
            l += len(label) + 2

        if isinstance(value, (list, tuple)):
            if isinstance(value[1], bool):
                if value[1]:
                    ctx.addstr(t, l, f'{value[0]}*', color)
                else:
                    ctx.addstr(t, l, str(value[0]), color)
            else:
                ctx.addstr(t, l, f'{value[0]} ({value[1]})', color)
        else:
            ctx.addstr(t, l, str(value), color | curses.A_BOLD)
