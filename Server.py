from Player import Player
from hashlib import sha256
from json import dumps, loads
from select import select
from socket import *
from threading import Thread


class Server:

    def __init__(self):
        # Set up variables

        # Map of player_id to sockets
        self.player_sockets = {}

        # Instance of Board class
        self.board = object()

        # Main socket port
        self.main_port = 44469

        # Main socket
        main_sock = socket()
        main_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        main_sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        main_sock.setblocking(0)
        main_sock.bind(('', self.main_port))
        print("Main Socket Bound")
        self.main_sock = main_sock

        # Polling socket port
        self.poll_port = 44470

        # Polling socket
        poll_sock = socket(AF_INET, SOCK_DGRAM)
        poll_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        poll_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        poll_sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        poll_sock.bind(('', self.poll_port))
        self.poll_sock = poll_sock

        # Password
        self.password = None

        # Created
        self.created = False

        Thread(target=self._create_listener).start()

    def close(self):
        # Cleanup for testing
        self.created = True
        self.main_sock.close()
        self.poll_sock.close()
        print("Closed")

    """
        Listeners
    """

    def _create_listener(self):
        # Have the main socket listen for CREATE messages
        self.main_sock.listen(10)
        print("Server Listening for CREATE messages")

        try:
            while not self.created:
                connections, w, x = select([self.main_sock], [], [], 0.05)

                for conn in connections:
                    client_sock, address = conn.accept()
                    message = client_sock.recv(4096).decode()
                    try:
                        data = loads(message)
                        # Check that the command is correct
                        if 'command' not in data or data['command'] != 'CREATE':
                            raise ValueError()

                        # Check for the necessary data, knowing the command is correct
                        if 'values' not in data or 'game' not in data['values'] or data['values']['game'] != 'Monopoly':
                            raise ValueError()

                        # Game Creation message obeys API for now, so try to get the necessary data
                        # Password will either be None or an encrypted text
                        self.password = data['values'].get('password', None)

                        # Create a Player object with a unique id with this username
                        username = data['values'].get('username', 'Guest')
                        player = Player(username)

                        # Send the player to the Board
                        # self.board.addPlayer(player)

                        # Store the player socket
                        self.player_sockets[player] = client_sock

                        # Inform the client of success
                        client_sock.sendall('0'.encode())

                        # Set created to True to escape loop
                        self.created = True
                    except ValueError:
                        client_sock.sendall('1'.encode())

            # Open the server
            # self._listen()
        except Exception as e:
            self.close()
            print(e)

    def _listen(self):
        # Open the polling socket
        print("Polling socket now open")
        polling_thread = Thread(target=self._poll_listener, daemon=True)
        polling_thread.start()

        # Make the main socket listen for new things

    """
        Message Sending Methods
    """

    def send_goto(self, player_id, tile):
        # Constructs and sends a GOTO message
        pass

    def send_pay(self, amount, player_from=None, player_to=None):
        # Constructs and sends a PAY message
        if player_from is None and player_to is None:
            raise ValueError("Monopoly - PAY: From and To cannot be None together")

    def send_card(self, card):
        # Constructs and sends a CARD message
        pass

    def send_turn(self, player_id):
        # Constructs and sends a TURN message
        pass

    def send_event(self, event_message):
        # Sends an event message through the CHAT feature
        pass