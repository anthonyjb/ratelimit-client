import os

__all__  = ('DungeonGenerator', )


class Dungeon:
    """
    A dungeon.
    """

    def __init__(self, size):

        self.size = size
        self.tiles = list('#' * (size[0] * size[1]))

    def draw_rect(self, tile, position, size):
        """Draw a rectangle within the dungeon of the given tile"""

        px, py = position

        for sy in range(size[1]):
            for sx in range(size[0]):

                x = px + sx
                y = py + sy

                if x < self.size[0] and y < self.size[1]:
                    self.tiles[x * y] = tile

    def render(self, filepath):
        """Render the dungeon to a file"""

        with open(filepath, 'w') as f:

            for y in range(self.size[1]):
                for x in range(self.size[0]):
                    f.write(self.tiles[x * y])
                f.write(os.linesep)


class DungeonGeneratorBSP:
    """
    Dungeon generator using binary space partitioning.

    [Ref: http://www.roguebasin.com/index.php/Basic_BSP_Dungeon_generation]
    """

    def __init__(
        self,
        dungeon_size=(80, 40),
        iteration_range=(2, 4),
        split_range=(0.25, 0.75),
    ):
        self.dungeon_size = dungeon_size
        self.iteration_range = iteration_range
        self.split_range = split_range

    def generate(self):

        dungeon = Dungeon(size=self.dungeon_size)

        return dungeon


if __name__ == '__main__':

    dungeon_generator = DungeonGeneratorBSP()
    dungeon = dungeon_generator.generate()
    dungeon.render('dungeon.txt')

#
# @
#
# - when creating rooms within partitions we need to ensure we leave enough
#   a gap or at least one tile so that rooms don't merge.
#
