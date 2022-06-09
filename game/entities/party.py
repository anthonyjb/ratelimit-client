import curses

from game.settings import settings
from game.ui.colors import Colors
from game.utils.rendering import in_bounds


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

    def render(self, ctx, offset, bounds):
        """Render the party"""

        offset_y = offset[0] + self.y
        offset_x = offset[1] + self.x

        if in_bounds(bounds, offset_y, offset_x):

            ctx.addch(
                offset_y,
                offset_x,
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
