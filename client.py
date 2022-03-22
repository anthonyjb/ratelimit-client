
import asyncio
import json

import toml


class Client:

    def __init__(self):

        # Load the connection settings for the game server
        with open('cfg/server.toml') as f:
            self._server_settings = toml.load(f)

    async def connect(self):
        """Connect to the game server"""
        self._reader, self._writer = await asyncio.open_connection(
            self._server_settings['host'],
            self._server_settings['port']
        )

    async def loop(self):
        await self.connect()

        while True:
            response = await self.send({'foo': 'bar'})
            print(response)
            await asyncio.sleep(1)

    async def send(self, message):
        """Send a message to the game server"""

        message_json = json.dumps(message)
        self._writer.write(message_json.encode())
        response = await self._reader.read(1024)

        return response


if __name__ == '__main__':

    client = Client()
    asyncio.run(client.loop())


# @@
# - Handle failures to connect
# - Detect lost connections
#   - Support attempts to reconnect

# - Ability to send

# - Check for input from the player
# - If input from the player
#   - Process input from the player

"""

Simplest single player case

    - Lets imagine at first that the on connecting to the server it already
      assigns me a player with a position. The game loop for a single player
      becomes simple

      - On connection we get the intial frame which will always be 0

      - ask the server what can I see for frame X (initially 0)
      - render what we can see for that frame
      - process player input (left, right, up, down or wait)
          - recieve response from server with next frame
      - loop forever


Multiplayer case (still simple)

    - Lets imagine this is the same as the single at start up, you are
      automatically given a player with a position. But this time you are
      also assigned a turn position. There are 2 players in our example and
      you are allocated the first turn which is turn position 0.

    - by default we set frame x to -1

    - On connection we get the initial frame, our turn position and the current
      turn.

    - if frame x is different to what it was last time we rendered
        - ask the server what can I see for frame X
        - render what we can see for that frame
    - if it is our turn
        - wait for player input
            - process player input
                - recieve response from server with current frame and turn
    - else
        - wait 1 second
        - ask the server what the current frame is and who's turn it is
        - if it is greater than the frame we have
            - update our frame by one (or support fetch all frames to this time)
    - loop


NPCs

    - Identical to simple multiplayer case accept there is always and NPC
      now in the turn positions so all games have effectively 2 players and
      turns must be respected.

    -




"""
