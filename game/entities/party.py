import curses

from game.settings import settings
from game.ui.colors import Colors


class Party:
    """
    The party of players.
    """

    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def char(self):
        return settings.overworld.party[0]

    @property
    def color_pair(self):
        return Colors.pair(settings.overworld.party[1], settings.ui.bg_color)

    def render(self, ctx):
        """Render the party"""

        ctx.addch(
            self.y,
            self.x,
            self.char,
            self.color_pair | curses.A_BOLD
        )

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to a `Party` instance"""

        party = Party()
        party.x = json_type['position'][0]
        party.y = json_type['position'][1]

        return party
