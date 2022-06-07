
from game.settings import settings

__all__= ['key_pressed']


def key_pressed(key_path, char):
    """Return true if char matches the given settings value"""

    value = settings
    for key in key_path.split('.'):
        value = getattr(value, key)

    if isinstance(value, list):
        return char in value

    return value == char
