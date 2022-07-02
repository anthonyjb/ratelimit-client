
import curses

from game.settings import settings


class Colors:

    _color_index = 8
    _color_pair_index = 1

    # A look up table of color pairs
    _color_pairs = {}

    @classmethod
    def add_color(cls, name, r, g, b):
        """Add a color to the games palette"""
        assert cls._color_index < 255, 'Too many colors defined.'
        assert not hasattr(cls, name), 'This name is already defined.'

        setattr(cls, name, cls._color_index)

        curses.init_color(
            cls._color_index,
            round(r / 255 * 1000),
            round(g / 255 * 1000),
            round(b / 255 * 1000)
        )

        cls._color_index += 1

    @classmethod
    def hex_to_rgb(cls, hex_color):
        """
        Return a RGB color (as a 3 item tuple) from a 3 or 6 character hex
        string.
        """
        if len(hex_color) == 3:
            return (
                int(hex_color[0], 16),
                int(hex_color[1], 16),
                int(hex_color[2], 16)
            )

        return (
            int(hex_color[0:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )

    @classmethod
    def init(cls):
        """
        Initialize the palette of colours that can be used within the game.
        """

        for name, hex_color in settings.colors.items():
            cls.add_color(name, *cls.hex_to_rgb(hex_color))

    @classmethod
    def pair(cls, fg, bg):
        """
        Add a color pair to the games palette (if not already present) and
        return it.
        """

        pair = (fg, bg)
        if pair not in cls._color_pairs:
            assert cls._color_pair_index < 65536, \
                    'Too many color pairs defined.'

            cls._color_pairs[(fg, bg)] = cls._color_pair_index
            curses.init_pair(
                cls._color_pair_index,
                getattr(cls, fg),
                getattr(cls, bg)
            )
            cls._color_pair_index += 1

        return curses.color_pair(cls._color_pairs[pair])
