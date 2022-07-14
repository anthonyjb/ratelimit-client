import curses
import math

from game.settings import settings
from game.utils.colors import Colors
from game.utils.sprites import SpriteSheet


class Scene:
    """
    The a scene within the game.
    """

    def __init__(self, size):
        self._size = size
        self._tiles = [SceneTile() for i in range(size[0] * size[1])]

        # The players
        self.players = None

    @property
    def size(self):
        return list(self._size)

    def get_tile(self, y, x=None):
        """Return a tile either by index or y,x coordinates."""
        if x is None:
            return self._tiles[y]
        return self._tiles[y * self._size[1] + x]

    def render(self, viewport):
        """Render the overworld"""

    def render_static(self, viewport):
        """
        Render static elements within the overworld.

        The overworld doesn't change in appearance so we can render it into the
        viewport just once.
        """

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to an `Overworld` instance"""

        size = [json_type['size'][1], json_type['size'][0]]
        tiles = json_type['tiles']


class SceneTile:
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
