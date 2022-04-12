import curses
import logging

from game.ui.component import Component


class InfoPanel(Component):
    """
    A UI component that displays pannel of information.
    """

    def __init__(self, width, height, title):
        super().__init__()

        # The curses window the panel will be added to
        self._width = width
        self._height = height
        self._title = title

        # @@ text / buttons

    def render(self, window):

        # Caclulate the size of the panel
        max_y, max_x = window.getmaxyx()

        width = self._width
        if width < 1:
            width = max_x + width

        height = self._height
        if height < 1:
            height = max_y + height

        # Calculate the position of the window
        x = (max_x - width) // 2
        y = (max_y - height) // 2

        height -= 1

        # Draw window
        window.hline(y, x, curses.ACS_HLINE, width)
        window.hline(y + height, x, curses.ACS_HLINE, width)
        window.vline(y, x, curses.ACS_VLINE, height)
        window.vline(y, x + width, curses.ACS_VLINE, height)
        window.addch(y, x, curses.ACS_ULCORNER)
        window.addch(y, x + width, curses.ACS_URCORNER)
        window.addch(y + height, x, curses.ACS_LLCORNER)
        window.addch(y + height, x + width, curses.ACS_LRCORNER)
        window.refresh()

# @@ Width and height against base UI component should handle width and height
#    based on distance from the right or bottom of parent window. If there is
#    no parent then the width / height of the parent will be assumed to be 0.
# @@ Create a root UI component against the game loop and have resize auto
#    update the size of this base component.
# @@ States should add there own root component to this game root component and
#    disable / hide the component when the games state is paused and remove it
#    when the game state is left (and viceversa).
# @@ Finish the info panel example
#
