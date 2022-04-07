import logging
import sys

from game.states.state import GameState
from game.ui.info_panel import InfoPanel


class FatalError(GameState):
    """
    If a fatal error occurs the game should switch to this state, informing the
    player of our calamitous mistake, and providing them with the option to
    send details of the error to us.

    Sometimes it probably isn't our mistake, if no error (exception is
    provided then there's nothing to send to us anyway so in those case we
    simply allow the player to quit the game.
    """

    ID = 'fatal_error'

    def enter(
        self,
        title='Great fudge! You borked it...',
        summary=(
            'You can help us figure this out by sending us the error details.'
            'If you are happy to help in this way select to send us the error '
            'below.'
        ),
        error=None,
        **kw
    ):
        super().enter(**kw)

        self.title = title
        self.summary = summary
        self.error = error

        # Log the error
        logging.exception('FATAL_ERROR', exc_info=True)

        # Set up the UI
        self.game.main_window.clear()
        self.info_panel = InfoPanel(-4, -2, self.title)
        self.info_panel.render(self.game.main_window)

    def leave(self):
        super().leave()
        del self.info_panel

    def input(self, char):
        super().input(char)

        # Quit the game
        self.game.quit = True

    def update(self, dt):
        super().update(dt)

    def render(self):
        super().render()


# @@
#
# - Create an information screen ui component that supports
    # - Title
    # - Text
    # - @@ Buttons
# - Create a button ui component that supports
    # - label
    # - on_select

# Should we render this UI per cycle or only once
