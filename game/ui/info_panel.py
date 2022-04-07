import curses
import curses.panel
import logging

class InfoPanel:
    """
    A UI component that displays pannel of information.
    """

    def __init__(self, width, height, title):

        # The curses window the panel will be added to
        self._width = width
        self._height = height
        self._title = title

        self._panel = None

        # @@ text / buttons

    def __del__(self):
        if self._panel:
            del self._panel
            del self._stack_panel

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


# A base UI component with the concept of children would be good here, also
# UI components should potentially support update and input not just render
# and we need a nice way to listen for events from a UI component like
# selecting a button.