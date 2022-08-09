import logging

__all__ = [
    'Viewport',
    'in_bounds'
]


class Viewport:
    """
    A viewport for efficiently rendering the game world.
    """

    def __init__(self):
        self.buffers = {}

    def blit(self, y, x, z, char, styles):
        """Blit a character to the viewport"""

        try:
            self.buffers[z][y][x] = (char, styles)
        except KeyError:
            try:
                self.buffers[z][y] = {}
                self.buffers[z][y][x] = (char, styles)
            except KeyError:
                self.buffers[z] = {}
                self.buffers[z][y] = {}
                self.buffers[z][y][x] = (char, styles)

    def clear(self, z=None):
        """Clear a buffer (or all buffers if z is None) within the viewport"""

        if z is None:
            self.buffers = {}

        else:
            self.buffers.pop(z, None)

    def render(self, ctx, position, size, offset):
        """Render the contents of the viewport"""

        # Determine the bounds of the content we can render in
        bounds = [
            offset[0],
            offset[1],
            offset[0] + size[0],
            offset[1] + size[1]
        ]

        # Render the viewport
        layers = sorted(self.buffers.keys())
        for z in layers:

            rows = self.buffers[z]
            for y in sorted(rows.keys()):
                if y < bounds[0]:
                    continue

                elif y > bounds[2]:
                    break

                columns = rows[y]
                for x in sorted(rows[y].keys()):
                    if x < bounds[1]:
                        continue

                    elif x > bounds[3]:
                        break

                    cell = columns.get(x)
                    if cell:

                        ry = position[0] + (y - offset[0])
                        rx = position[1] + (x - offset[1])

                        ctx.addch(
                            ry,
                            rx,
                            cell[0],
                            cell[1]
                        )


def in_bounds(bounds, y, x):
    """Return true if y and z are within the given bounds"""

    return (
        y >= bounds[0]
        and y <= bounds[2]
        and x >= bounds[1]
        and x <= bounds[3]
    )
