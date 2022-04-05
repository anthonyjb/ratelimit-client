
import asyncio
import json
import logging
import uuid

from game.settings import settings


class GameServerClient:
    """
    The game server client provides an interface for connect to and
    communicating with the game server.
    """

    def __init__(self):
        self._reader = None
        self._writer = None

    async def connect(self):
        """Connect to the game server"""

        # @@ handle sConnectionRefusedError
        self._reader, self._writer = await asyncio.open_connection(
            settings.server.host,
            settings.server.port
        )

        # Register
        r = await self.send(
            'handshake',
            {
                'uid': uuid.getnode(),
                'password': settings.server.password
            }
        )

        logging.info(f'Connection response')

    async def send(self, message_type, message):
        """Send a message to the game server"""

        # Build the message to send
        json_data = json.dumps({
            'id': str(uuid.uuid4()),
            'type': message_type,
            'message': message
        }).encode()

        return await self._send(json_data)

    async def _send(self, json_data):
        """
        Send a message to the game server (private function that can
        recursively call itself in an attempt to deal with failed attempts to
        send a message or receive a response.
        """

        try:
            self._writer.write(json_data)
            response = await self._reader.read(1024)
            return json.loads(response or '{}')

        except (
            asyncio.exceptions.IncompleteReadError,
            asyncio.exceptions.TimeoutError
        ):

            # Try again after a short delay
            await asyncio.sleep(1)

            response = await self._send(json_data)
            return json.loads(response or '{}')

        except asyncio.exceptions.InvalidStateError:

            # Attempt to reconnect and send again after a short delay
            await asyncio.sleep(1)
            await self.connect()
            response = await self._send(json_data)
            return json.loads(response or '{}')
