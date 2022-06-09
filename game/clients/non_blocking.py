
import asyncio
import json
import logging
import struct
import uuid

from game.settings import settings


class NonBlockingClient:
    """
    The `NonBlockingClient` provides an interface for connecting to and
    communicating with the game server that does not block the game loop when
    making a request to wait for a response.
    """

    def __init__(self):
        self._reader = None
        self._writer = None
        self._connected = False

    @property
    def connected(self):
        return self._connected

    async def connect(self):
        """Connect to the game server"""

        future = asyncio.open_connection(
            settings.server.host,
            settings.server.port
        )
        try:
            self._reader, self._writer = await asyncio.wait_for(
                future,
                timeout=5
            )
        except asyncio.TimeoutError:
            logging.info('Connect timed out')

        logging.info(settings.server.node or uuid.getnode())

        # Register
        r = await self.send(
            'handshake',
            {
                'node': settings.server.node or uuid.getnode(),
                'password': settings.server.password
            }
        )

        self._connected = True

    async def send(self, message_type, message=None):
        """Send a message to the game server"""

        # Build the message to send
        json_data = json.dumps({
            'uid': str(uuid.uuid4()),
            'type': message_type,
            'message': message
        }).encode()

        return await self._send(json_data)

    async def _send(self, json_data):
        self._writer.write(struct.pack('>I', len(json_data) * 4))
        self._writer.write(json_data)

        response_len = struct.unpack('>I', await self._reader.read(4))[0]
        remaining = response_len

        response = b''
        while remaining > 0:
            response += await self._reader.read(remaining)
            remaining = response_len - len(response) * 4

        return json.loads(response.decode('utf8') or '{}')

        # try:
        #     response = await asyncio.wait_for(future, timeout=5)
        #     return json.loads(response or '{}')

        # except (
        #     asyncio.exceptions.IncompleteReadError,
        #     asyncio.exceptions.TimeoutError
        # ):
        #     return

        #     # Try again after a short delay
        #     await asyncio.sleep(1)

        #     response = await self._send(json_data)
        #     return json.loads(response or '{}')

        # except asyncio.exceptions.InvalidStateError:
        #     return

        #     # Attempt to reconnect and send again after a short delay
        #     await asyncio.sleep(1)
        #     await self.connect()
        #     response = await self._send(json_data)
        #     return json.loads(response or '{}')

# Allow server timeout period to be configured

# @@
#
# - Add ability to set the node ID in settings so we can run multiple clients
#   on our own machines
#
