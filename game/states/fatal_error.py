import logging
import sys
import urllib
import webbrowser

from game.states.manager import GameStateManager
from game.states.state import GameState
from game.ui.button import Button
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
            'You can help us figure this mystery out by sending us the error '
            'details. Select <Y> and we\'ll open your email client with a '
            'prepopulated email you can send to us. To be clear we wont share '
            'your email with anyone else or use it to contact you about '
            'anything other than this issue unless you\'ve signed up to '
            'receive emails for some other reason.'
        ),
        error=None,
        allow_send_error=True,
        **kw
    ):
        super().enter(**kw)

        self.title = title
        self.summary = summary
        self.error = error

        # Log the error
        logging.exception('FATAL_ERROR', exc_info=True)

        # Add info panel to the UI displayed
        info_panel = InfoPanel(title, summary)
        self.ui_root.add_child(info_panel)
        info_panel.left = 5
        info_panel.right = 5

        # Set up buttons for the info panel
        if allow_send_error:

            yes_button = Button('Sure thing', 'y')
            yes_button.add_event_listener('select', self.on_yes)
            info_panel.buttons.add_child(yes_button)

            no_button = Button('No thanks', 'n')
            no_button.add_event_listener('select', self.on_no)
            info_panel.buttons.add_child(no_button)

        else:

            ok_button = Button('Okay', 'any')
            ok_button.add_event_listener('select', self.on_no)
            info_panel.buttons.add_child(ok_button)

        info_panel.buttons.layout('row', 2)
        info_panel.buttons.fit_content()

    def on_no(self, event):
        self.game.quit = True

    def on_yes(self, event):

        qs = urllib.parse.urlencode({
            'to': 'ant@getme.co.uk',
            'subject': 'Error report...',
            'body': self.error
        })

        webbrowser.open(f'mailto:?{qs}', new=1)

        self.game.quit = True

GameStateManager.register(FatalError)
