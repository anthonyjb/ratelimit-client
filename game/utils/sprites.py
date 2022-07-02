
from game.settings import settings
from game.utils.colors import Colors


class Sprite:
    """
    A sprite that can be rendered in the overworld or a scene.
    """

    def __init__(self, id, descriptor, character, color):

        self.id = id
        self.descriptor = descriptor
        self.character = character
        self.color = color

    def __str__(self):
        return f'{self.descriptor} ({self.character}, {self.color})'

    @property
    def color_pair(self):
        return Colors.pair(self.color, settings.ui.bg_color)


class SpriteSheet:
    """
    The SpriteSheet class provides functionality for rendering the overworld
    and scenes as described by the server.

    The sprite sheet is a tree, the initial teir of which contains the core
    entity types:

    In the overworld:
        - biomes
        - landmarks

    In scenes:
        - terrain
        - scenary
        - items
        - creatures

    Under each tier each entity is described in up to 3 levels, for example:

        - biomes
            - woodland
                - evergreen
                    - ancient

    The sprite sheet allows us to get the character and color pair to use when
    rendering an enitiy described as above. The sprite sheet allows for partial
    matches, so for example if a tile in the overworld has the following biome:

        - woodland, broadleaf, ancient

    But we only have a definition for:

        - woodland, broadleaf

    Then the character and color pair returned will be for woodland broadleaf
    as a fallback, if we didn't have a broadleaf entry then we'd fall back to
    just a woodland character.

    This allows new entities to be added into the game that client is yet
    unaware but still allowing the new entitiy to be rendered in it's closest
    matching form.

    To be clear; the sprite sheet is defined by the server, the character and
    color used for each sprite is defined in the clients sprites cfg file.
    """

    def __init__(self):
        self._sprites = {

            # Overworld
            'biomes': {},
            'landmarks': {},

            # Scenes
            'terrain': {},
            'scenary': {},
            'creatures': {},
            'items': {}

        }
        self._fallback = None

    def set_fallback(self, sprite):
        """
        Set the sprite to return when there are no matches for a given sprite
        path.
        """
        self._fallback = sprite

    def add(self, base_type, path, sprite):
        """Add a sprite to the sheet"""
        self._sprites[base_type][path] = sprite

    def get(self, base_type, path):
        """Return a sprite based on the given path"""
        while path:
            try:
                return self._sprites[base_type][path]
            except KeyError:
                path = tuple(path[0:-1])
        return self._fallback

    @classmethod
    def from_json_type(self, json_type):
        """Convert a JSON type object to a `SpriteSheet` instance"""

        sprite_sheet = SpriteSheet()

        sprite_sheet.set_fallback(
            Sprite(
                0,
                'unknown',
                *settings.sprites['fallback']
            )
        )

        for base_type in sprite_sheet._sprites:
            entries = [(
                None,
                [],
                json_type.get(base_type, {}).get('types', {})
            )]

            while entries:
                descriptor_path, id_path, sprite_types = entries.pop(0)

                for descriptor, sprite_type in sprite_types.items():

                    sub_descriptor_path = descriptor
                    if descriptor_path:
                        sub_descriptor_path = '__'.join([
                            descriptor_path,
                            descriptor
                        ])

                    sub_id_path = id_path + [sprite_type['id']]

                    if sub_descriptor_path in settings.sprites[base_type]:

                        sprite_sheet.add(
                            base_type,
                            tuple(sub_id_path),
                            Sprite(
                                sprite_type['id'],
                                descriptor,
                                *settings\
                                        .sprites[base_type][sub_descriptor_path]
                            )
                        )

                    if sprite_type.get('types'):
                        entries.append(
                            (
                                sub_descriptor_path,
                                sub_id_path,
                                sprite_type['types']
                            )
                        )

        return sprite_sheet
