import curses


class GameLoop:
    """
    The game loop is responsible for executing the game's logic continuously.
    """

    def init(self):
        """Initialize key systems for the game"""

        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        self.screen.keypad(True)
        self.main_window = curses.newwin(*self.screen.getmaxyx(), 0, 0)

    def run(self):

        try:

            while True:
                self.main_window.timeout(1000 // 60)

                key = self.main_window.getch()

        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up before exiting the game"""

        self.screen.keypad(False)
        curses.curs_set(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


