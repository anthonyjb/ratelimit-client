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
    LEFT = 3
    Right = 8

    def __init__(self, point):
        super().__init__()

        self.point = point

    def update(self, dt):

        # Vertical anchor

        if TOP & self.point:

            pass

        elif BOTTOM & self.point:

            pass

        else: # CENTER

            pass

        # Horizontal anchor

        if LEFT & self.point:

            pass

        elif RIGHT & self.point:

            pass

        else: # CENTER

            pass

