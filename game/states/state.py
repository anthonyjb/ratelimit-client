
class GameState:
    """
    A base class for defining different game states. The flow of the game is
    managed by the `GameStateManager` which transitions the game between
    various `GameState`s.
    """

    def __init__(self):
        pass

    def enter(self, **kwargs):
        """
        Called when the game enter the state which then becomes the active
        state.
        """

    def leave(self):
        """
        Called when the game leaves this state.
        """

    def pause(self, new_state_id):
        """
        Called when the game pauses this state before transitioning to
        another.
        """

    def resume(self, **kwargs):
        """Called when the game transitiong back to the paused state"""

    def input(self, char):
        """Handle the given user input for the state"""

    def update(self, dt, paused):
        """
        Update the state based on the time ellapsed between now and the
        previous call to update.
        """

    def render(self):
        """Render the state's visual representation to the screen"""
