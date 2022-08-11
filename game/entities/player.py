import curses

from game.settings import settings
from game.utils.colors import Colors


class Player:
    """
    The player.
    """

    def __init__(self):
        self.name = 'unknown'
        self.race = 'unknown'
        self.profession = 'unknown'

        self.x = 0
        self.y = 0
        self.action_points = [0, 0]

    @property
    def yx(self):
        return [self.y, self.x]

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to a `Party` instance"""

        player = Player()

        # Descriptive
        player.name = json_type['name']
        player.race = json_type['race']
        player.profession = json_type['profession']

        # Stats
        player.action_points = json_type['action_points']

        # Coordinates
        player.x = json_type['position'][0]
        player.y = json_type['position'][1]

        return player
