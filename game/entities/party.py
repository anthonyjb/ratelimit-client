import curses

from game.settings import settings
from game.utils.colors import Colors
from game.utils.player import get_player_uid


class Party:
    """
    The party of players.
    """

    def __init__(self):
        self.members = []
        self.leader = None

        self.x = 0
        self.y = 0

    @property
    def char(self):
        return '@'

    @property
    def color_pair(self):
        return Colors.pair('snow', settings.ui.bg_color)

    @property
    def i_am_leader(self):
        return get_player_uid() == self.leader

    def render(self, viewport):
        """Render the party"""

        viewport.blit(
            self.y,
            self.x,
            1,
            self.char,
            self.color_pair | curses.A_BOLD
        )

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to a `Party` instance"""

        party = Party()

        party.members = json_type['members']
        party.leader = json_type['leader']

        party.x = json_type['position'][0]
        party.y = json_type['position'][1]

        return party
