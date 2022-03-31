from game.states.state import GameState


class InGame(GameState):
    """
    The in-game state provides a viewport into the game world, showing either
    the overworld or underworld (a scene) and allowing a player perform
    actions within the game world (such as move north, attack goblin).
    """

    ID = 'in_game'

    def enter(self, **kw):
        super().enter(**kw)

        print('entered')

    def leave(self):
        super().leave()

        print('left')

    def input(self, char):
        super().input(char)

    def update(self, dt):
        super().update(dt)

    def render(self):
        super().render()
