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

    @property
    def size(self):
        return list(self._size)

    def apply_scene_changes(self, scene_changes):
        """Apply a set of scene changes to the overworld"""

        for tile_index, sprites in scene_changes.items():
            terrain, scenary, item, creature = sprites

            tile = self.get_tile(int(tile_index))

            if terrain == -1:
                tile.terrain = None
            else:
                tile.terrain = tuple(terrain)

            if scenary == -1:
                tile.scenary = None
            else:
                tile.scenary = tuple(scenary)

            if item == -1:
                tile.item = None
            else:
                tile.item = tuple(item)

            if creature == -1:
                tile.creature = None
            else:
                tile.creature = tuple(creature)

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
        """Render the scene"""

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

        scene = cls(size)
        for y in range(size[0]):
            for x in range(size[1]):

                tile_index = y * size[1] + x
                terrain, scenary, items, creatures = tiles[tile_index]
                tile = scene.get_tile(tile_index)

                if terrain != -1:
                    tile.terrain = tuple(terrain)

                if scenary != -1:
                    tile.scenary = tuple(scenary)

                if items != -1:
                    tile.items = tuple(items)

                if creatures != -1:
                    tile.creatures = tuple(creatures)

        return scene


class SceneTile:
    """
    A tile within the scene.
    """

    def __init__(self, terrain=None, scenary=None, items=None, creatures=None):

        self.terrain = terrain
        self.scenary = scenary
        self.items = items
        self.creatures = creatures

    @property
    def character(self):
        sprites = SpriteSheet.singleton()

        if self.creatures:
            return sprites.get('creatures', self.creatures).character

        if self.items:
            return sprites.get('items', self.items).character

        if self.scenary:
            return sprites.get('scenary', self.scenary).character

        if self.terrain:
            return sprites.get('terrain', self.terrain).character

    @property
    def color_pair(self):
        sprites = SpriteSheet.singleton()

        if self.creatures:
            return sprites.get('creatures', self.creatures).color_pair

        if self.items:
            return sprites.get('items', self.items).color_pair

        if self.scenary:
            return sprites.get('scenary', self.scenary).color_pair

        if self.terrain:
            return sprites.get('terrain', self.terrain).color_pair

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
