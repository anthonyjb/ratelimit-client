
__all__ = ['in_bounds']


def in_bounds(bounds, y, x):
    """Return true if y and z are within the given bounds"""
    return (
        y >= bounds[0]
        and y <= bounds[2]
        and x >= bounds[1]
        and x <= bounds[3]
    )
