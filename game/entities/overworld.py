import curses

from game.settings import settings
from game.ui.colors import Colors


class Overworld:
    """
    The game's overworld.
    """

    def __init__(self, size):
        self._size = size
        self._tiles = [OverworldTile() for i in range(size[0] * size[1])]

    @property
    def size(self):
        return list(self._size)

    def get_tile(self, y, x=None):
        """Return a tile either by index or y,x coordinates."""
        if x is None:
            return self._tiles[y]
        return self._tiles[y * self._size[1] + x]

    def render(self, ctx):
        """Render the overworld"""

        size = self.size

        for y in range(size[0]):
            for x in range(size[1]):
                tile_index = y * size[1] + x
                self._tiles[tile_index].render(ctx, y, x)

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to an `Overworld` instance"""

        size = [json_type['size'][1], json_type['size'][0]]
        landmarks = json_type['landmarks']
        terrains = json_type['terrains']
        tiles = json_type['tiles']

        overworld = Overworld(size)
        for y in range(size[0]):
            for x in range(size[1]):

                tile_index = y * size[1] + x
                terrain, landmark = tiles[tile_index]
                tile = overworld.get_tile(tile_index)

                if terrain > -1:
                    tile.terrain = terrains[terrain]

                if landmark > -1:
                    tile.landmark = landmarks[landmark]

        return overworld


class OverworldTile:
    """
    A tile within the game's overworld.
    """

    def __init__(self, terrain=None, landmark=None):
        self.terrain = terrain
        self.landmark = landmark

    @property
    def char(self):
        if self.landmark:
            return settings.overworld.landmarks[self.landmark][0]

        if self.terrain:
            return settings.overworld.terrains[self.terrain][0]

    @property
    def color_pair(self):

        if self.landmark:
            return Colors.pair(
                settings.overworld.landmarks[self.landmark][1],
                settings.ui.bg_color
            )

        if self.terrain:
            return Colors.pair(
                settings.overworld.terrains[self.terrain][1],
                settings.ui.bg_color
            )

    def render(self, ctx, y, x):
        """Render the tile"""

        if self.char:
            ctx.insch(y, x, self.char, self.color_pair | curses.A_BOLD)