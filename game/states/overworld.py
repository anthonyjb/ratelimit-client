import curses
import logging

from game import entities
from game.settings import settings
from game.states.state import GameState
from game.utils.colors import Colors
from game.utils.input import key_pressed
from game.utils.rendering import Viewport


class Overworld(GameState):
    """
    A view of the game overworld which the party can navigate around. The
    overworld state should only be entered from the in-game state.
    """

    ID = 'overworld'

    def enter(self, **kw):
        super().enter(**kw)

        self.overworld = None
        self.party = None
        self.last_frame_no = -1
        self.replay_dt = 0

        # A viewport to render the game world within
        self.viewport = Viewport()

        # Bootstraps
        self.game.bootstrap(
            'Fetching overworld...',
            lambda: self.fetch_overworld()
        )

    def input(self, char):
        super().input(char)

        if not self.party.i_am_leader:
            return

        if key_pressed(f'controls.enter_scene', char):
            self.enter_scene()

        for direction, key in enumerate(settings.controls.directions.keys()):
            if key_pressed(f'controls.directions.{key}', char):
                self.move_party(direction)

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

        # Clear dynamic layer for viewport
        self.viewport.clear(z=1)

        # Render the dynamic elements within the overworld
        self.overworld.render(self.viewport)

        # Draw the viewport's content
        viewport_rect = [2, 1, max_y - 9, max_x - 3]

        self.viewport.render(
            ctx,
            viewport_rect[0:2],
            viewport_rect[2:],
            self.overworld.get_offset(self.party.yx, [max_y - 8, max_x - 4])
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

    def enter_scene(self):
        """Attempt to enter the scene the party is currently located over"""
        response = self.game.client.send('party:enter_scene')
        if response['success']:
            self.game_state_manager.pop(in_scene=True)

    def move_party(self, direction):
        """Move the party in the given direction"""
        response = self.game.client.send('move', {'direction': direction})

        # Immediately move the player as we control them
        if 'position' in response:
            self.party.x = response['position'][0]
            self.party.y = response['position'][1]
            self.my_turn = True

    def move_to_frame_no(self, frame):
        """Move to the given frame within the overworld"""

        frame = self.game.frames[self.last_frame_no]

        actor = frame.get('actor')
        action = frame.get('action')
        data = frame.get('data')
        scene_changes = frame.get('scene_changes')

        if actor == 'party':

            if action == 'move':

                # Move the party to the position they are in for this frame
                self.party.x = data['position'][0]
                self.party.y = data['position'][1]

                # Update the overworld with any scene changes
                self.overworld.apply_scene_changes(scene_changes)
                self.overworld.render(self.viewport)

            elif frame.get('action') == 'enter_scene':

                # Party has entered a scene, transition the game to the scene
                # state.
                self.game_state_manager.pop(in_scene=True)

    def sync_frame(self, dt):
        """Sync the """

        if self.party.i_am_leader:

            # If are the party leader then our party is already in the correct
            # position (as we are the only one who can move it) so just sync
            # the frame no.
            self.last_frame_no = self.game.frame_no
            return

        # We are not the party leader and therefore the sync is passive and may
        # involve catching up several frames.

        if self.last_frame_no == -1:

            # When the player first enters the overworld we always show the
            # most recent frame (no catch up on entering the overworld).
            self.last_frame_no = self.game.frame_no

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

    def fetch_overworld(self):
        """Fetch the overworld from the server"""
        self.overworld = entities.overworld.Overworld.from_json_type(
            self.game.client.send('world:read')
        )

        self.party = entities.party.Party.from_json_type(
            self.game.client.send('party:read')
        )

        self.overworld.party = self.party

        # Render the overworld to the viewport
        self.overworld.render(self.viewport)
