
import uuid

from game.settings import settings

__all__ = ['get_player_uid']


def get_player_uid():
    """Return the player UID"""
    return settings.server.node or uuid.getnode()
