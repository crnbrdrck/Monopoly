from .Server import Server
from json import *
from select import select
from socket import *

class TestCreate:

    def test_failure(self):
        """
            Cases:
                1. No Command
                2. Command not CREATE
                3. No values
                4. Game not in values
                5. Wrong game in values
        """
        # Create a server
        server = Server()

        # Create a socket
        sock = socket()
        sock.connect(('localhost', 44469))

        payload = dumps({})
        sock.sendall(payload.encode())

        # Wait for reply
        print("Waiting for response of 1")
        try:
            while True:
                connections, w, x = select([sock], [], [], 1)

                for conn in connections:
                    client, addr = sock.accept()

                    data = client.recv(4096).decode()
                    assert data == "1"
                    break
                    
        except KeyboardInterrupt:
            print("Took too long to respond")
        finally:
            server.close()
            sock.close()
