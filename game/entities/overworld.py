import curses
import math

from game.settings import settings
from game.utils.colors import Colors
from game.utils.sprites import SpriteSheet


class Overworld:
    """
    The game's overworld.
    """

    def __init__(self, size):
        self._size = size
        self._tiles = [OverworldTile() for i in range(size[0] * size[1])]

        # The player party
        self.party = None

    @property
    def size(self):
        return list(self._size)

    def get_offset(self, size):
        """
        Return the offset to render at so that the party is in view of the
        given viewport.
        """

        h = size[0]
        w = size[1]

        y = self.party.y - round(h / 2)
        x = self.party.x - round(w / 2)

        y = max(0, min(y, self.size[0] - h))
        x = max(0, min(x, self.size[1] - w))

        return [y, x]

    def get_tile(self, y, x=None):
        """Return a tile either by index or y,x coordinates."""
        if x is None:
            return self._tiles[y]
        return self._tiles[y * self._size[1] + x]

    def render(self, viewport):
        """Render the overworld"""

        self.party.render(viewport)

    def render_static(self, viewport):
        """
        Render static elements within the overworld.

        The overworld doesn't change in appearance so we can render it into the
        viewport just once.
        """

        h = self.size[0]
        w = self.size[1]

        for y in range(h):
            for x in range(w):
                self._tiles[y * w + x].render(viewport, y, x)

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to an `Overworld` instance"""

        size = [json_type['size'][1], json_type['size'][0]]
        tiles = json_type['tiles']

        overworld = Overworld(size)
        for y in range(size[0]):
            for x in range(size[1]):

                tile_index = y * size[1] + x
                biome, landmark = tiles[tile_index]
                tile = overworld.get_tile(tile_index)

                if biome != -1:
                    tile.biome = tuple(biome)

                if landmark != -1:
                    tile.landmark = tuple(landmark)

        return overworld


class OverworldTile:
    """
    A tile within the game's overworld.
    """

    def __init__(self, biome=None, landmark=None):

        self.landmark = landmark
        self.biome = biome

    @property
    def character(self):
        sprites = SpriteSheet.singleton()

        if self.landmark:
            return sprites.get('landmarks', self.landmark).character

        if self.biome:
            return sprites.get('biomes', self.biome).character

    @property
    def color_pair(self):
        sprites = SpriteSheet.singleton()

        if self.landmark:
            return sprites.get('landmarks', self.landmark).color_pair

        if self.biome:
            return sprites.get('biomes', self.biome).color_pair

    def render(self, viewport, y, x):
        """Render the tile"""

        if self.character:
            viewport.blit(
                y,
                x,
                0,
                self.character,
                self.color_pair | curses.A_BOLD
            )
