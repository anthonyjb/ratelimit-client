import curses

from game.settings import settings
from game.utils.colors import Colors


class Player:
    """
    The player.
    """

    def __init__(self):
        self.x = 0
        self.y = 0

    @property
    def yx(self):
        return [self.y, self.x]

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to a `Party` instance"""

        party = Player()
        party.x = json_type['position'][0]
        party.y = json_type['position'][1]

        return party
