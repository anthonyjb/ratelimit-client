
import curses


class Colors:

    _color_index = 0
    _color_pair_index = 0

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
            (r // 255) * 1000,
            (g // 255) * 1000,
            (b // 255) * 1000
        )

        cls._color_index += 1

    @classmethod
    def pair(cls, fg, bg):
        """Add a color pair to the games palette"""

        pair = (fg, bg)
        if pair not in cls._color_pairs:
            assert cls._color_pair_index < 65536, 'Too many color pairs defined.'

            cls._color_pairs[(fg, bg)] = cls._color_pair_index
            curses.init_pair(
                cls._color_pair_index,
                getattr(cls, fg),
                getattr(cls, bg)
            )
            cls._color_index += 1

        return cls._color_pairs[pair]

    @classmethod
    def init(cls):
        """
        Initialize the palette of colours that can be used within the game.
        """
        cls.add_color('CORNSILK', 241, 236, 206)
        cls.add_color('DARK_PURPLE', 51, 24, 50)

        # @@ Add code to load colors from a config file
