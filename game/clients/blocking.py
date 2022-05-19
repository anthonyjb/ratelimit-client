
import json
import logging
import socket
import struct
import uuid

from game.settings import settings


class BlockingClient:
    """
    The `BlockingClient` provides an interface for connecting to and
    communicating with the game server that blocks the game loop when making a
    request to wait for a response.
    """

    def __init__(self):
        self._socket = None
        self._connected = False

    @property
    def connected(self):
        return self._connected

    def connect(self):
        """Connect to the game server"""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((settings.server.host, settings.server.port))

        # Register
        r = self.send(
            'handshake',
            {
                'node': uuid.getnode(),
                'password': settings.server.password
            }
        )

        self._connected = True

    def send(self, message_type, message=None):
        """Send a message to the game server"""

        # Build the message to send
        json_data = json.dumps({
            'uid': str(uuid.uuid4()),
            'type': message_type,
            'message': message
        }).encode('utf8')

        return self._send(json_data)

    def _send(self, json_data):
        self._socket.sendall(struct.pack('>I', len(json_data) * 4))
        self._socket.sendall(json_data)

        response_len = struct.unpack('>I', self._socket.recv(4))[0]
        remaining = response_len

        response = b''
        while remaining > 0:
            response += self._socket.recv(remaining)
            remaining = response_len - len(response) * 4

        return json.loads(response.decode('utf8') or '{}')
