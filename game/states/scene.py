import curses
import logging

from game import entities
from game.settings import settings
from game.states.state import GameState
from game.utils.colors import Colors
from game.utils.input import key_pressed
from game.utils.player import get_player_uid
from game.utils.rendering import Viewport


class Scene(GameState):
    """
    A view of the a scene (e.g a dungeon, village, woodland) within the game
    the party has entered. The scene state should only be entered from the
    in-game state.
    """

    ID = 'scene'

    @property
    def is_my_turn(self):
        return self.active_player == get_player_uid()

    def enter(self, **kw):
        super().enter(**kw)

        self.active_player = kw['active_player']
        self.last_frame_no = self.game.frame_no
        self.player = None
        self.replay_dt = 0
        self.scene = None

        # A viewport to render the game world within
        self.viewport = Viewport()

        # Bootstraps
        self.game.bootstrap(
            'Fetching scene...',
            lambda: self.fetch_scene()
        )

    def input(self, char):
        super().input(char)

        if not self.is_my_turn:
            return

        logging.info(str(char))

        if key_pressed(f'controls.end_turn', char):
            self.end_turn()

        for direction, key in enumerate(settings.controls.directions.keys()):
            if key_pressed(f'controls.directions.{key}', char):
                self.move_player(direction)

    def update(self, dt):
        super().update(dt)

        if self.paused:
            return

        self.sync_frame(dt)

    def render(self):

        if self.paused:
            return

        ctx = self.game.main_window

        max_y, max_x = self.game.main_window.getmaxyx()

        # Clear the viewport
        self.viewport.clear()

        # Render the dynamic elements within the overworld
        self.scene.render(self.viewport)

        # Draw the viewport's content
        viewport_rect = [2, 1, max_y - 9, max_x - 3]

        self.viewport.render(
            ctx,
            viewport_rect[0:2],
            viewport_rect[2:],
            self.scene.get_offset(self.player.yx, [max_y - 8, max_x - 4])
        )

        # Draw the viewport border
        t = 1
        l = 0
        b = viewport_rect[2] + 3
        r = viewport_rect[3] + 2

        border_color = Colors.pair('coyote', settings.ui.bg_color)
        ctx.hline(t, l, curses.ACS_HLINE, r, border_color)
        ctx.hline(b, l, curses.ACS_HLINE, r, border_color)
        ctx.vline(t, l, curses.ACS_VLINE, b, border_color)
        ctx.vline(t, r - 1, curses.ACS_VLINE, b, border_color)

        corner_color = Colors.pair('independence', settings.ui.bg_color)
        ctx.addch(t, l, '┏', corner_color)
        ctx.addch(t, r - 1, '┓', corner_color)
        ctx.addch(b, l, '┗', corner_color)
        ctx.addch(b, r - 1, '┛', corner_color)

        super().render()

    # Non-lifecycle methods

    def end_turn(self):
        """End the players turn"""
        self.game.client.send('player:end_turn')

    def move_player(self, direction):
        """Move the player in the given direction"""
        self.game.client.send('move', {'direction': direction})

    def move_to_frame_no(self, frame):
        """Move to the given frame within the scene"""

        frame = self.game.frames[self.last_frame_no]

        actor = frame.get('actor')
        action = frame.get('action')
        data = frame.get('data')
        scene_changes = frame.get('scene_changes')

        self.active_player = data['active_player']

        if self.is_my_turn:

            if actor == 'party':

                if action == 'move':

                    # Move the player to the position they are in for this frame
                    self.player.x = data['position'][0]
                    self.player.y = data['position'][1]

        # Update the scene with any scene changes
        if scene_changes:
            self.scene.apply_scene_changes(scene_changes)
            self.scene.render(self.viewport)

    def sync_frame(self, dt):
        """Sync view to the current frame"""

        max_frame_lag = settings.game.max_frame_lag
        if self.last_frame_no < (self.game.frame_no - max_frame_lag):

            # Don't allow the player to lag too far behind the current game
            # frame.

            while self.last_frame_no < (self.game.frame_no - max_frame_lag):

                # Increment the frame by one
                self.last_frame_no += 1

                # Apply the frame
                self.move_to_frame_no(self.last_frame_no)

        if self.last_frame_no < self.game.frame_no:

            # The player is currently behind the most recent game frame so
            # replay past frames to catch up.
            self.replay_dt += dt

            if self.replay_dt > 1 / settings.game.replay_frame_rate:

                # Increment the frame by one
                self.last_frame_no += 1

                # Apply the frame
                self.move_to_frame_no(self.last_frame_no)

    # Bootstraps

    def fetch_scene(self):
        """Fetch the scene from the server"""
        self.scene = entities.scene.Scene.from_json_type(
            self.game.client.send('scene:read')
        )

        self.player = entities.player.Player.from_json_type(
            self.game.client.send('player:read')
        )

# @@ Create a UI component for the viewport border as this code is
# reported.
