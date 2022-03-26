
class GameStateManager:
    """
    The game state manager is responsible for transitioning the game between
    different states the updating all states in the current state stack once
    per game loop iteration.
    """

    def __init__(self):
        pass

    def collapse(self, state):
        """
        Remove all states in the stack currently and replace them with the
        given state.
        """

    def pop(self, **kw):
        """Remove the current scene from the stack"""

    def push(self, **kw):
        """Push a new scene onto the stack making it the current scene"""

    def register(self, scene):
        """Register a scene with the game sate manager"""

    def input(self, char):
        """Handle the given user input for the current state"""

    def update(self, dt):
        """Update all states currently in the stack"""

    def render(self, dt):
        """Render the current state"""
