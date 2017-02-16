from Server import Server
from hashlib import sha256
from json import *
from socket import *

class TestCreate:

    def _send_message(self, message, server):
        """
        Sends a message to a server and returns the result
        :param message: The message to be sent
        :param server: The server to send the message to
        :return: The response from the server
        """
        sock = socket()
        while True:
            try:
                sock.connect(('', server.main_port))
                break
            except:
                pass
        sock.sendall(message.encode())
        data = sock.recv(4096).decode()

        # Close socket and return data
        sock.close()
        return data

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
        print("Case 1: No command key in payload")
        assert self._send_message(dumps({}), server) == '1'

        print("Case 2: Command value != 'CREATE'")
        assert self._send_message(dumps({'command': 'BUY'}), server) == "1"

        print("Case 3: No values key in payload")
        assert self._send_message(dumps({'command': 'CREATE'}), server) == "1"

        print("Case 4: No game key in values")
        assert self._send_message(dumps({'command': 'CREATE', 'values': {}}), server) == "1"

        print("Case 5: Wrong game value")
        assert self._send_message(dumps({'command': 'CREATE', 'values': {'game': 'Not Monopoly'}}), server) == '1'

        server.close()

    def test_create(self):
        """
            Cases:
                1. All Correct values, but no username or password
                2. All correct values with username and no password
                3. All correct values with username and password
        """
        print("Case 1: All Correct Values, no username or password")
        while True:
            try:
                server = Server()
                break
            except:
                pass
        sock = socket()
        while True:
            try:
                sock.connect(('', server.main_port))
                break
            except:
                pass
        print("Socket connected")
        try:
            # Send a CREATE request with no username or password
            payload = {'command': 'CREATE', 'values': {'game': 'Monopoly'}}
            sock.sendall(dumps(payload).encode())
            assert sock.recv(4096).decode() == '0'
            # Check that the Player object is correct in the socket map
            for k in server.player_sockets:
                # There should only be one key
                if k.getUsername() != 'Guest':
                    raise AssertionError()
            assert server.password is None
        except:
            raise
        finally:
            print("Test completed, closing connections - 95")
            server.close()
            sock.close()

        print("Case 2: All Correct Values with username and no password")
        while True:
            try:
                server = Server()
                break
            except:
                pass
        sock = socket()
        while True:
            try:
                sock.connect(('', server.main_port))
                break
            except:
                pass
        print("Socket connected")
        try:
            # Send a CREATE request with a username but no password
            payload = {'command': 'CREATE', 'values': {'game': 'Monopoly', 'username': 'Test'}}
            sock.sendall(dumps(payload).encode())
            assert sock.recv(4096).decode() == '0'
            # Check that the Player object is correct in the socket map
            for k in server.player_sockets:
                # There should only be one key
                if k.getUsername() != payload['values']['username']:
                    raise AssertionError()
            assert server.password is None
        except:
            raise
        finally:
            print("Test completed, closing connections - 128")
            server.close()
            sock.close()

        print("Case 3: All Correct Values with username and no password")
        while True:
            try:
                server = Server()
                break
            except:
                pass
        sock = socket()
        while True:
            try:
                sock.connect(('', server.main_port))
                break
            except:
                pass
        print("Socket connected")
        try:
            # Send a CREATE request with a username and password
            password = sha256('hi'.encode()).hexdigest()
            payload = {'command': 'CREATE', 'values': {'game': 'Monopoly', 'username': 'Test', 'password': password}}
            sock.sendall(dumps(payload).encode())
            assert sock.recv(4096).decode() == '0'
            # Check that the Player object is correct in the socket map
            for k in server.player_sockets:
                # There should only be one key
                if k.getUsername() != payload['values']['username']:
                    raise AssertionError()
            assert server.password == password
        except:
            raise
        finally:
            print("Test completed, closing connections - 162")
            server.close()
            sock.close()

if __name__ == '__main__':
    TestCreate().test_failure()
    TestCreate().test_create()
