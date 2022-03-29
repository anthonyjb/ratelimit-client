
class GameState:
    """
    A base class for defining different game states. The flow of the game is
    managed by the `GameStateManager` which transitions the game between
    various `GameState`s.
    """

    # The ID of the state
    ID = 'game_state'

    # Possible statuses for a game state
    READY = 0
    ACTIVE = 1
    PAUSED = 2

    def __init__(self, gameStateManager):

        self._gameStateManager = gameStateManager
        self._status = self.READY

    @property
    def status(self):
        return self._status

    def enter(self, **kwargs):
        """
        Called when the game enter the state which then becomes the active
        state.
        """

        assert (
            self.status == self.READY,
            'State can only be entered if status is READY.'
        )

        self._status = self.ACTIVE

    def leave(self):
        """
        Called when the game leaves this state.
        """

        assert (
            self.status == self.ACTIVE or self.status == self.PAUSED,
            'State can only be left if status is ACTIVE or PAUSED.'
        )

        self._status = self.READY

    def pause(self, new_state_id):
        """
        Called when the game pauses this state before transitioning to
        another.
        """

        assert (
            self.status == self.ACTIVE,
            'State can only be paused if status is ACTIVE.'
        )

        self._status = self.PAUSED

    def resume(self, **kwargs):
        """Called when the game transitiong back to the paused state"""

        assert (
            self.status == self.PAUSED,
            'State can only be resumed if status is PAUSED.'
        )

        self._status = self.ACTIVE

    def input(self, char):
        """Handle the given user input for the state"""

    def update(self, dt, paused):
        """
        Update the state based on the time ellapsed between now and the
        previous call to update.
        """

    def render(self):
        """Render the state's visual representation to the screen"""
