import curses
import time

from game import settings
from game import states


class GameLoop:
    """
    The game loop is responsible for executing the game's logic continuously.
    """

    def init(self):
        """Initialize key systems for the game"""

        # Set up the screen
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        self.screen.keypad(True)

    @property
    def main_window(self):
        return self._main_window

    @property
    def screen(self):
        return self._screen

    async def run(self):

        try:

            # Set up the main window for the game
            self._main_window = curses.newwin(*self.screen.getmaxyx(), 0, 0)

            # Register the game states
            GSM = states.GameStateManager
            GSM.register(states.in_game.InGame)

            # Set up the game state manager
            self._state_manager = GSM(self)
            self._state_manager.push('in_game')

            # Run the game loop
            self.quit = False

            last_loop_time = time.time()
            while not self.quit:
                char = self.main_window.getch()

                if char == curses.ERR:
                    await asyncio.sleep(0.1)

                elif char == curses.KEY_RESIZE:
                    pass # @@ TODO: Handle the console being resized

                else:
                    self._state_manager.input(char)

                self._state_manager.update(time.time() - last_loop_time)
                self._state_manager.render()

                last_loop_time = time.time()

        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up before exiting the game"""

        self.screen.keypad(False)
        curses.curs_set(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()


# @@
#
# - Plan how we will join a game through the client.
# - Create a bootstrap state?
#
