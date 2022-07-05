import asyncio
import curses
import logging
import os
import socket
import time
import traceback

from game.clients.blocking import BlockingClient
from game.clients.non_blocking import NonBlockingClient
from game.settings import settings
from game import states
from game.states.manager import GameStateManager
from game.ui.component import Component
from game.ui.console import Console
from game.utils.colors import Colors
from game.utils.sprites import SpriteSheet


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

        # These two numbers indicate the last frame we have stored in the
        # client vs. the last frame on the server.
        self._client_frame_no = -1
        self._server_frame_no = 0

        # A table of frames received from the server
        self._frames = {}

    @property
    def client(self):
        return self._blocking_client

    @property
    def frame_no(self):
        return self._client_frame_no

    @property
    def frames(self):
        return self._frames

    @property
    def main_window(self):
        return self._main_window

    @property
    def screen(self):
        return self._screen

    @property
    def sprite_sheet(self):
        return self._sprite_sheet

    @property
    def ui_console(self):
        return self._ui_console

    @property
    def ui_root(self):
        return self._ui_root

    async def run(self):

        try:
            # Set up the main window for the game
            self._main_window = curses.newwin(*self.screen.getmaxyx(), 0, 0)
            self._main_window.nodelay(True)
            self._main_window.keypad(True)

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

            # Set up development console UI component
            self._ui_console = Console()
            self._ui_root.add_child(self._ui_console)

            # Set up the game state manager
            self._state_manager = GameStateManager(self)

            # Create a client and attempt to connect to the game server
            self._blocking_client = BlockingClient()
            self._non_blocking_client = NonBlockingClient()

            try:
                self._blocking_client.connect()
                await self._non_blocking_client.connect()

                # Set the initial game state
                self._state_manager.push('in_game')

                # Load the sprite sheet from the server
                self._state_manager.push(
                    'bootstrap',
                    message='Fetching sprite sheet...',
                    task=lambda: self.fetch_sprite_sheet()
                )

            except (Exception, ConnectionRefusedError, socket.gaierror) as error:
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
            peek_task = None
            last_peek_time = time.time() - 1
            last_loop_time = time.time()
            while not self.quit:
                self._ui_console.clear()

                char = self.main_window.getch()
                curses.flushinp()

                if char == curses.ERR:
                    await asyncio.sleep(0.1)

                elif char == curses.KEY_RESIZE:
                    self.on_resize()

                else:
                    self.ui_console.input(char)
                    self._state_manager.input(char)

                dt = time.time() - last_loop_time
                self._state_manager.update(dt)
                self._ui_console.update(dt)

                self.main_window.erase()
                self._state_manager.render()

                if self._non_blocking_client.connected:

                    if (
                        not peek_task or peek_task.done()
                        and last_peek_time > 1
                    ):
                        # Peek
                        peek_task = asyncio.ensure_future(self.peek())
                        last_peek_time = time.time()

                # NOTE: Must be the last line in the loop
                self._ui_console.render(self.main_window)


        finally:
            self.cleanup()

    async def peek(self):
        """Peek at the current frame number on the server"""

        self._server_frame_no \
                = (await self._non_blocking_client.send('peek'))['frame_no']

        # If the server frame number is now greater than the client frame
        # number fetch the frames that have elapsed.

        if self._client_frame_no < self._server_frame_no:

            new_frames = (await self._non_blocking_client.send(
                'get_frames',
                {'frame_no': self._client_frame_no + 1}
            ))['frames']

            self._frames.update({f[0]: f[1] for f in new_frames})
            self._client_frame_no = self._server_frame_no

    def cleanup(self):
        """Clean up before exiting the game"""

        self.screen.keypad(False)
        curses.curs_set(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def fetch_sprite_sheet(self):
        """Fetch the sprite sheet from the server"""
        SpriteSheet.from_json_type(self.client.send('sprite_sheet:read'))

    def on_resize(self):
        """Handle the console being resized"""

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

# @@
# - Establish how let both ends know the length of content we are sending
#   about to receive).

# - Create a sync client along with the async client
# - We will have async and sync clients
# - read until new line, parse content-length: number, read content length data

# @@ PEEK (asyncio)
#   - Request no more than once a second
#   - Returns the current frame and which players turn it is, response is not
#     waited for and the task will update the current frame / turn info against
#     the game loop (potentially triggering a request for frames to playback).
#   - Asyncio so as to not delay current loop while IO between server and client

# @@ ALL OTHER COMMANDS (syncio)
#   - Request on demand
#   - Wait for response
#
