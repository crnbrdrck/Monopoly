from json import *
from socket import *

from Server import Server


def send_message(message, port, sock_type=SOCK_STREAM):
    """
    Sends a message to a server and returns the result
    :param message: The message to be sent
    :param port: The port to send the message to
    :param sock_type: The type of socket to be created. Default TCP
    :return: The response from the server
    """
    sock = socket(AF_INET, sock_type)
    while True:
        try:
            sock.connect(('', port))
            break
        except:
            pass
    sock.sendall(message.encode())
    data = sock.recv(4096).decode()

    # Close socket and return data
    sock.close()
    return data


class TestCreate:

    def test_create(self):
        """
            Cases:
                1. No Command
                2. Command not CREATE
                3. No values
                4. Game not in values
                5. Wrong game in values
                6. Actual CREATE message to see that the server starts up
        """
        # Create a server
        server = Server()

        # Create a socket
        print("Case 1: No command key in payload")
        assert send_message(dumps({}), server._main_port) == '1'

        print("Case 2: Command value != 'CREATE'")
        assert send_message(dumps({'command': 'BUY'}), server._main_port) == "1"

        print("Case 3: No values key in payload")
        assert send_message(dumps({'command': 'CREATE'}), server._main_port) == "1"

        print("Case 4: No game key in values")
        assert send_message(dumps({'command': 'CREATE', 'values': {}}), server._main_port) == "1"

        print("Case 5: Wrong game value")
        assert send_message(dumps({'command': 'CREATE', 'values': {'game': 'Not Monopoly'}}), server._main_port) == '1'

        print("Case 6: Actual CREATE message to test success")
        assert send_message(dumps({'command': 'CREATE', 'values': {'game': 'Monopoly'}}), server._main_port) == '0'
        # Check that the Player object is correct in the socket map
        for k in server._player_sockets:
            # There should only be one key
            if k.getUsername() != 'Guest':
                raise AssertionError()
        assert server._password is None

        server.close()

class TestPoll:

    # Set up a server that has been properly created
    def test_configure(self):
        while True:
            try:
                self.server = Server()
                break
            except:
                pass
        sock = socket()
        while True:
            try:
                sock.connect(('', self.server._main_port))
                break
            except:
                pass
        payload = {'command': 'CREATE', 'values': {'game': 'Monopoly', 'username': 'Test'}}
        sock.sendall(dumps(payload).encode())
        assert sock.recv(4096).decode() == '0'
        sock.close()

    def test_failure(self):
        """
        Cases:
            1. No Command
            2. Command not CREATE
            3. No values
            4. Game not in values
            5. Wrong game in values
        """
        print("Case 1: No command key in payload")
        assert send_message(dumps({}), self.server._poll_port, SOCK_DGRAM) == '1'

        print("Case 2: Command value != 'POLL'")
        assert send_message(dumps({'command': 'CREATE'}), self.server._poll_port, SOCK_DGRAM) == "1"

        print("Case 3: No values key in payload")
        assert send_message(dumps({'command': 'POLL'}), self.server._poll_port, SOCK_DGRAM) == "1"

        print("Case 4: No game key in values")
        assert send_message(dumps({'command': 'POLL', 'values': {}}), self.server._poll_port, SOCK_DGRAM) == "1"

        print("Case 5: Wrong game value")
        assert send_message(dumps({'command': 'POLL', 'values': {'game': 'Not Monopoly'}}),
                            self.server._poll_port,
                            SOCK_DGRAM) == '1'

    def test_success(self):
        """
            Case:
                1. Correct command and value
        """

        print("POLL should return password: False and players: ['Test']")
        data = send_message(dumps({'command': 'POLL', 'values': {'game': 'Monopoly'}}),
                            self.server._poll_port,
                            SOCK_DGRAM)
        data = loads(data)
        assert 'command' in data and data['command'] == 'GAME'
        assert 'values' in data
        assert 'password' in data['values'] and data['values']['password'] == False
        assert 'players' in data['values'] and data['values']['players'] == ['Test']

    # Close the server after the tests finish
    def test_unconfigure(self):
        self.server.close()


if __name__ == '__main__':
    print("Test Create")
    t = TestCreate()
    t.test_create()
    print()
    print("Test Poll")
    t = TestPoll()
    t.test_configure()
    t.test_failure()
    print()
    t.test_success()
    print()
    t.test_unconfigure()
