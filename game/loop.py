import asyncio
import curses
import logging
import os
import socket
import time
import traceback

from game.client import GameServerClient
from game.settings import settings
from game import states
from game.states.manager import GameStateManager
from game.ui.colors import Colors
from game.ui.component import Component


class GameLoop:
    """
    The game loop is responsible for executing the game's logic continuously.
    """

    def init(self):
        """Initialize key systems for the game"""

        self.quit = False

        # Setup a log file for the game
        logging.basicConfig(
            filename='logs/game.log',
            level=logging.DEBUG
        )
        logging.getLogger('asyncio').setLevel(logging.WARNING)

        # Set up the screen
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        curses.start_color()
        self.screen.keypad(True)

    @property
    def client(self):
        return self._client

    @property
    def main_window(self):
        return self._main_window

    @property
    def screen(self):
        return self._screen

    @property
    def ui_root(self):
        return self._ui_root

    async def run(self):

        try:
            # Set up the main window for the game
            self._main_window = curses.newwin(*self.screen.getmaxyx(), 0, 0)
            self._main_window.nodelay(True)

            # Initialize the game's color palette
            Colors.init()
            self._main_window.bkgd(
                ' ',
                Colors.pair(settings.ui.fg_color, settings.ui.bg_color)
            )

            # Set up a root UI component for the game
            self._ui_root = Component()
            self._ui_root.add_tag('game_root')
            self.on_resize()

            # Set up the game state manager
            self._state_manager = GameStateManager(self)
            self._state_manager.push('in_game')

            # Create a client and attempt to connect to the game server
            self._client = GameServerClient()

            try:
                await self._client.connect()
            except (ConnectionRefusedError, socket.gaierror) as error:
                self._state_manager.collapse(
                    'fatal_error',
                    title='Server is hiding...',
                    summary=(
                        'Unable to connect to the game server, if you are '
                        'running it locally check it\'s erm... running, if '
                        'you are connecting to a remote host blame them '
                        'continously until you spot your typo in the '
                        'settings file at which point exclaim it is now '
                        'miraculously working.'
                    ),
                    allow_send_error=False
                )

            # Run the game loop
            last_loop_time = time.time()
            while not self.quit:
                char = self.main_window.getch()

                if char == curses.ERR:
                    await asyncio.sleep(0.1)

                elif char == curses.KEY_RESIZE:
                    self.on_resize()

                else:
                    self._state_manager.input(char)

                self._state_manager.update(time.time() - last_loop_time)
                self.main_window.clear()
                self._state_manager.render()

                # @@ Peek say once a second

        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up before exiting the game"""

        self.screen.keypad(False)
        curses.curs_set(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def on_resize(self):
        """Handle the console being resized"""

        if not settings.ui.display_resizable:

            # Attempt (or pray) to fix the display size

            # Window
            os.system(f'mode {settings.ui.display[0]},{settings.ui.display[1]}')

            # MacOS / Linux
            os.system(
                f'resize -s {settings.ui.display[1]} {settings.ui.display[0]}'
            )

            # MacOS / Linux
            print(f'\x1b[8;{settings.ui.display[1]};{settings.ui.display[0]}t')

        # Update the root UI size to that of the main window
        max_y, max_x = self.main_window.getmaxyx()
        self._ui_root.width = max_x
        self._ui_root.height = max_y


# @@
#
# - Handle failure to connect to the game server graciously (in the client,
#   check response and if not a valid connection raise an error we can
#   capture in-game and deal with (e.g unable to connect to game server please
#   check your settings).
# - Handle auto-reconnections
# - Plan how we will join a game through the client.
# - Create a bootstrap state?
#
