import curses
import logging

from game import entities
from game.settings import settings
from game.states.state import GameState
from game.ui.border import Border
from game.ui.stats import StatBar, Stat
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

        # Set up a border for the viewport
        self.border = Border()
        self.border.right = 0
        self.border.top = 1
        self.ui_root.add_child(self.border)

        # Set up a stat bar
        self.stat_bar = StatBar()
        self.ui_root.add_child(self.stat_bar)

        self.stats = {
            'name': Stat(('unknown', False)),
            'action_points': Stat(
                ('?', '?'),
                'AP',
                settings.ui.stats_bar.action_points_color
            )
        }

        for stat in self.stats.values():
            self.stat_bar.add_child(stat)

        # Bootstraps
        self.game.bootstrap(
            'Fetching scene...',
            lambda: self.fetch_scene()
        )

    def input(self, char):
        super().input(char)

        if not self.is_my_turn:
            return

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

        self.stats['action_points'].value = self.player.action_points

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

        # Update the height of the border to wrap the viewport
        self.border.height = viewport_rect[2] + 2

        # Update the position of the start bar to be under the viewport
        self.stat_bar.top = viewport_rect[2] + 3

        # Update the UI to show who's turn it currently is

        if self.is_my_turn:
            turn_str = 'My turn'
        else:
            # @@ This should be displaying the name of the player or entity
            # who's turn it is.
            turn_str = 'Not my turn'

        ctx.addstr(0, max_x - len(turn_str), turn_str, curses.A_ITALIC)

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

            self.player.action_points = data['action_points']

            if actor == 'player':

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

        self.stats['name'].value = (
            f'{self.player.name} '
            f'({self.player.race} {self.player.profession})'
        )


# - Display when it's another entities turn
