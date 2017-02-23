from json import dumps, loads
from select import select
from socket import *
from threading import Thread

from Player import Player


class Server:

    # The max number of players allowed in the lobby
    _MAX_PLAYERS = 8

    # The max wait for the 'select' methods
    _SELECT_TIMEOUT = 0.05

    def __init__(self):
        # Set up variables

        # Map of Player objects to sockets
        self._player_sockets = {}

        # Reverse map of sockets to Player objects
        self._socket_owners = {}

        # Instance of Board class
        self._board = object()

        # Main socket port
        self._main_port = 44469

        # Main socket
        main_sock = socket()
        main_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            main_sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        except:
            pass
        main_sock.setblocking(0)
        main_sock.bind(('', self._main_port))
        print("Main Socket Bound")
        self._main_sock = main_sock

        # Polling socket port
        self._poll_port = 44470

        # Polling socket
        poll_sock = socket(AF_INET, SOCK_DGRAM)
        poll_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        poll_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            poll_sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        except:
            pass
        poll_sock.bind(('', self._poll_port))
        self._poll_sock = poll_sock

        # Password
        self._password = None

        # Created
        self._created = False

        # Started
        self._started = False

        # Polling Thread
        self._polling_thread = Thread(target=self._poll_listener, daemon=True)

        self._main_thread = Thread(target=self._create_listener)
        self._main_thread.start()

    def close(self):
        # Cleanup for testing
        self._created = True
        self._started = True
        self._main_sock.close()
        self._poll_sock.close()
        print("Closed")

    """
        Listeners
    """

    def _create_listener(self):
        # Have the main socket listen for CREATE messages
        self._main_sock.listen(10)
        print("Server Listening for CREATE messages")

        try:
            while not self._created:
                connections, w, x = select([self._main_sock], [], [], Server._SELECT_TIMEOUT)

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
                        self._password = data['values'].get('password', None)

                        # Create a Player object with a unique id with this username
                        username = data['values'].get('username', 'Guest')
                        player = Player(username)

                        # Send the player to the Board
                        # self._board.addPlayer(player)

                        # Store the player socket
                        self._player_sockets[player] = client_sock
                        self._socket_owners[client_sock] = player

                        # Inform the client of success
                        client_sock.sendall('0'.encode())

                        # Don't close client_sock since we'll be using it to communicate with the client

                        # Set _created to True to escape loop
                        self._created = True
                    except ValueError as e:
                        print(e)
                        client_sock.sendall('1'.encode())
                        client_sock.close()

            # Open the server
            print("Server Open")
            self._pre_game_listen()

        except Exception as e:
            print("Closing due to exception:", e)
            self.close()

        finally:
            return

    def _pre_game_listen(self):
        # Open the polling socket
        print("Polling socket now open")
        self._polling_thread.start()

        # Make the main socket listen for new things
        self._main_thread = Thread(target=self._start_listener)
        self._main_thread.start()
        self._join_listener()

    def _poll_listener(self):
        # Listen for POLL requests
        while not self._started:
            data, addr = self._poll_sock.recvfrom(4096)
            try:
                data = loads(data.decode())
                # Check for matching API
                # Check for command value
                if 'command' not in data or data['command'] != 'POLL':
                    raise ValueError()

                # Check for values
                if 'values' not in data or 'game' not in data['values'] or data['values']['game'] != 'Monopoly':
                    raise ValueError()

                # If it reached this point, construct and send server data
                msg = self._generate_message(
                    'GAME',
                    password=self._password is not None,
                    players=[p.getUsername() for p in self._player_sockets]
                )
                # Send the game data back to the person asking
                self._poll_sock.sendto(msg.encode(), addr)

            except:
                self._poll_sock.sendto('1'.encode(), addr)
        print("Poll Socket Closing")
        return

    def _join_listener(self):
        """
        Listens for join requests
        """

        # Check for valid values
        while not self._started:
            connections, w, x = select([self._main_sock], [], [], Server._SELECT_TIMEOUT)

            for conn in connections:
                client_sock, address = conn.accept()
                message = client_sock.recv(4096).decode()
                try:
                    data = loads(message)

                    if 'command' not in data or data['command'] != 'JOIN':
                        raise ValueError()

                    values = data['values']
                    if 'game' not in values or values['game'] != 'Monopoly':
                        raise ValueError()
                    if 'password' not in values or values['password'] != self._password:
                        raise ValueError()
                    # Check if lobby is full
                    if len(self._player_sockets) == Server._MAX_PLAYERS:
                        raise ValueError()

                    # At this point it's safe to say the JOIN request is valid
                    username = values.get('username', 'Guest')
                    player = Player(username)

                    # Send the player to the Board
                    # self._board.addPlayer(player)

                    # Store the player socket
                    self._player_sockets[player] = client_sock
                    self._socket_owners[client_sock] = player

                    # Inform the client of success
                    client_sock.sendall('0'.encode())

                except ValueError:
                    client_sock.sendall('1'.encode())
                    client_sock.close()

    def _start_listener(self):
        """
        Listens for start request
        """

        # Check for valid values
        while not self._started:
            client_sockets = self._socket_owners.keys()
            connections, w, x = select(client_sockets, [], [], Server._SELECT_TIMEOUT)

            for conn in connections:
                message = conn.recv(4096).decode()
                try:
                    data = loads(message)

                    if 'command' not in data or data['command'] != 'START':
                        raise ValueError()

                    # Check the number of players in game, should be >= 2
                    if len(self._player_sockets) >= 2:
                        # Start the game
                        # Send start messages to everybody
                        msg = self._generate_message('START')
                        self._send_to_all(msg)
                        self._started = True
                    else:
                        raise ValueError()

                except ValueError:
                    conn.sendall('1'.encode())

    """
        Message Sending Methods
    """

    def send_turn(self, player: Player):
        # Constructs and sends a TURN message
        msg = self._generate_message('TURN', player=player.getId())
        self._send_to_all(msg)

    def send_goto(self, player: Player, tile: int):
        # Constructs and sends a GOTO message
        msg = self._generate_message('TURN', player=player.getId(), tile=tile)
        self._send_to_all(msg)

    def send_pay(self, amount, player_from=None, player_to=None):
        # Constructs and sends a PAY message
        try:
            if player_from is None and player_to is None:
                raise ValueError("Monopoly - PAY: From and To cannot be None together")
            msg = self._generate_message(
                'PAY',
                amount=amount,
                player_from=player_from.getId(),
                player_to=player_to.getId())
            self._send_to_all(msg)
        except Exception as e:
            print(e)

    def send_card(self, card):
        # Constructs and sends a CARD message
        msg = self._generate_message('CARD', text=card.getText(), is_bail=card.isBail())
        self._send_to_all(msg)

    def send_event(self, event_message):
        # Sends an event message through the CHAT feature
        msg = self._generate_message('CHAT', player=None, text=event_message)
        self._send_to_all(msg)

    def _send_to_all(self, msg: str):
        # Sends 'message' to all players in game
        for sock in self._socket_owners:
            sock.sendall(msg.encode())

    def _generate_message(self, command: str, **values: dict):
        # Returns a message dumped with the passed command and values
        return dumps(
            {
                'command': command,
                'values': values
            }
        )