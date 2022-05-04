
from game.states.manager import GameStateManager
from game.ui.component import Component


class RegisterGameState(type):
    """
    Meta class to register child classes of GameState with the
    GameStateManager.
    """

    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)

        if cls.ID != 'game_state':
            GameStateManager.register(cls)


class GameState(metaclass=RegisterGameState):
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

    # UI enabled and visible on pause
    PAUSED_UI_ENABLED = False
    PAUSED_UI_VISIBLE = False

    def __init__(self, game_state_manager):

        self._game_state_manager = game_state_manager
        self._status = self.READY
        self._ui_root = None

    @property
    def game(self):
        return self.game_state_manager.game

    @property
    def game_state_manager(self):
        return self._game_state_manager

    @property
    def status(self):
        return self._status

    @property
    def ui_root(self):
        return self._ui_root

    def enter(self, **kw):
        """
        Called when the game enter the state which then becomes the active
        state.
        """

        assert self.status == self.READY, \
            'State can only be entered if status is READY.'

        # Add root UI component
        self._ui_root = Component()
        self._ui_root.add_tag('state_root')
        self._ui_root.bottom = 0
        self._ui_root.right = 0
        self.game.ui_root.add_child(self._ui_root)

        # Set the state to active
        self._status = self.ACTIVE

    def leave(self):
        """
        Called when the game leaves this state.
        """

        assert self.status == self.ACTIVE or self.status == self.PAUSED, \
            'State can only be left if status is ACTIVE or PAUSED.'

        # Remove root UI component
        self.game.ui_root.remove_child(self._ui_root)
        del self._ui_root

        # Set state to ready
        self._status = self.READY

    def pause(self, new_state_id):
        """
        Called when the game pauses this state before transitioning to
        another.
        """

        assert self.status == self.ACTIVE, \
            'State can only be paused if status is ACTIVE.'

        self.ui_root.enabled = self.__class__.PAUSED_UI_ENABLED
        self.ui_root.visible = self.__class__.PAUSED_UI_VISIBLE
        self._status = self.PAUSED

    def resume(self, **kw):
        """Called when the game transitiong back to the paused state"""

        assert self.status == self.PAUSED, \
            'State can only be resumed if status is PAUSED.'

        self.ui_root.enabled = True
        self.ui_root.visible = True
        self._status = self.ACTIVE

    def input(self, char):
        """Handle the given user input for the state"""

        if chr(char) == "q":
            self.game.quit = True

        if self.ui_root:
            self.ui_root.input(char)

    def update(self, dt):
        """
        Update the state based on the time ellapsed between now and the
        previous call to update.
        """

        if self.ui_root:
            self.ui_root.update(dt)

    def render(self):
        """Render the state's visual representation to the screen"""

        if self.ui_root:
            self.ui_root.render(self.game.main_window)
