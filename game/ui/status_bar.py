import curses
import textwrap

from game.ui.anchor import Anchor
from game.ui.component import Component


class StatusBar(Component):
    """
    A UI component displayed at the top of the page that provides top level
    player/party status information.

    The bar is made up of 2 parts:

    - Observerd (e.g terrain type, landmark type)
    - Party (who's turn is it, what is there position within the party and
      who many members are there in the party).

    """

    def __init__(self, title, body):
        super().__init__()

    def update(self, dt):

        super().update(dt)

    def render(self, ctx):

        super().render(ctx)

