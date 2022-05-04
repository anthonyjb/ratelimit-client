import curses
from enum import Flag, auto
import textwrap

from game.settings import settings
from game.ui.colors import Colors
from game.ui.component import Component


class Anchor(Component):
    """
    A component that will anchor itself to the given anchor point of its
    parent.
    """

    # Possible anchor points, if an anchor point isn't provided for a given
    # direction then the point will be assumed to be centered.
    TOP = 1
    BOTTOM = 2
    LEFT = 4
    RIGHT = 8

    def __init__(self, point):
        super().__init__()

        self.point = point

    def update(self, dt):

        rect = self.rect
        parent_rect = self.parent.rect

        # Vertical anchor

        if self.TOP & self.point:
            self.top = 0

        elif self.BOTTOM & self.point:
            self.top = parent_rect[2] - rect[2]

        else: # CENTER
            self.top = round((parent_rect[2] - rect[2]) / 2)

        # Horizontal anchor

        if self.LEFT & self.point:
            self.left = 0

        elif self.RIGHT & self.point:
            self.left = parent_rect[3] - rect[3]

        else: # CENTER
            self.left = round((parent_rect[3] - rect[3]) / 2)
