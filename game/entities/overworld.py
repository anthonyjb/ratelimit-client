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

    @property
    def size(self):
        return list(self._size)

    def apply_scene_changes(self, scene_changes):
        """Apply a set of scene changes to the overworld"""

        # import logging
        # logging.info(str(scene_changes))

        for tile_index, sprites in scene_changes.items():
            biome, landmark, party = sprites

            tile = self.get_tile(int(tile_index))

            if biome == -1:
                tile.biome = None
            else:
                tile.biome = tuple(biome)

            if landmark == -1:
                tile.landmark = None
            else:
                tile.landmark = tuple(landmark)

            if party == -1:
                tile.party = None
            else:
                tile.party = tuple(party)

    def get_offset(self, yx, size):
        """
        Return the offset to render at so that the yx coordinate (e.g the
        player/party position) is in view of the given viewport.
        """

        h = size[0]
        w = size[1]

        y = yx[0] - round(h / 2)
        x = yx[1] - round(w / 2)

        y = max(0, min(y, self.size[0] - h))
        x = max(0, min(x, self.size[1] - w))

        return [y, x]

    def get_tile(self, y, x=None):
        """Return a tile either by index or y,x coordinates"""
        if x is None:
            return self._tiles[y]
        return self._tiles[y * self._size[1] + x]

    def render(self, viewport):
        """Render the overworld"""

        h = self.size[0]
        w = self.size[1]

        for y in range(h):
            for x in range(w):
                self._tiles[y * w + x].render(viewport, y, x)

    @classmethod
    def from_json_type(cls, json_type):
        """Convert a JSON type object to an `Overworld` instance"""

        size = [json_type['size'][1], json_type['size'][0]]
        tiles = json_type['tiles']

        overworld = cls(size)
        for y in range(size[0]):
            for x in range(size[1]):

                tile_index = y * size[1] + x
                biome, landmark, party = tiles[tile_index]
                tile = overworld.get_tile(tile_index)

                if biome != -1:
                    tile.biome = tuple(biome)

                if landmark != -1:
                    tile.landmark = tuple(landmark)

                if party != -1:
                    tile.party = tuple(party)

        return overworld


class OverworldTile:
    """
    A tile within the game's overworld.
    """

    def __init__(self, biome=None, landmark=None, party=None):

        self.landmark = landmark
        self.biome = biome
        self.party = party

    @property
    def character(self):
        sprites = SpriteSheet.singleton()

        if self.party:
            return sprites.get('parties', self.party).character

        if self.landmark:
            return sprites.get('landmarks', self.landmark).character

        if self.biome:
            return sprites.get('biomes', self.biome).character

    @property
    def color_pair(self):
        sprites = SpriteSheet.singleton()

        if self.party:
            return sprites.get('parties', self.party).color_pair

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
