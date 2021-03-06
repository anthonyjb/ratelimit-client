
class GameStateManager:
    """
    The game state manager is responsible for transitioning the game between
    different states the updating all states in the current state stack once
    per game loop iteration.
    """

    # A list of possible states for the game (named)
    _state_classes = []

    def __init__(self, game):

        # An instance of the game using the game state manager
        self._game = game

        # Initialize every registered state
        self._states = {}
        for state_cls in self._state_classes:
            self._states[state_cls.ID] = state_cls(self)

        # A stack representing the current state of the game with the first
        # item in the stack representing the current state and subsequent
        # items in the stack representing paused states.
        self._state = []

    @property
    def current_state(self):
        if self._state:
            return self._state[0]

    @property
    def game(self):
        return self._game

    @property
    def size(self):
        return len(self._state)

    def collapse(self, state_id, **kw):
        """
        Remove all states in the stack currently and replace them with the
        given state.
        """

        while self.current_state:
            self._state.pop(0).leave()

        self.push(state_id, **kw)

    def pop(self, **kw):
        """Remove the current scene from the stack"""

        self._state.pop(0).leave()

        if self.current_state:
            self.current_state.resume(**kw)

    def push(self, state_id, **kw):
        """Push a new scene onto the stack making it the current scene"""

        if self.current_state:
            self.current_state.pause(state_id)

        self._state.insert(0, self._states[state_id])
        self.current_state.enter(**kw)

    def input(self, char):
        """Handle the given user input for the current state"""
        self.current_state.input(char)

    def update(self, dt):
        """Update all states currently in the stack"""
        self.current_state.update(dt)

    def render(self):
        """Render the current state"""
        self.current_state.render()

    @classmethod
    def register(cls, state_cls):
        """Register a possible state with the game state manager class"""
        cls._state_classes.append(state_cls)
