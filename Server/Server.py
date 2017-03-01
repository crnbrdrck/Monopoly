from json import dumps, loads
from select import select
from socket import *
from threading import Thread

from Card import Card
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

    def close(self) -> None:
        # Cleanup for testing
        self._created = True
        self._started = True
        self._main_sock.close()
        self._poll_sock.close()

    """
        Listeners
    """

    def _create_listener(self) -> None:
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

    def _pre_game_listen(self) -> None:
        # Open the polling socket
        print("Polling socket now open")
        self._polling_thread.start()

        # Make the main socket listen for new things
        self._main_thread = Thread(target=self._start_listener)
        self._main_thread.start()
        self._join_listener()

    def _poll_listener(self) -> None:
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

    def _join_listener(self) -> None:
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

    def _start_listener(self) -> None:
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
                        msg = {
                            'command': 'START',
                            'values': {
                                'players': [{player.getId(): player.getUsername()} for player in self._player_sockets]
                            }
                        }
                        for sock, player in self._socket_owners.items():
                            msg['values']['local'] = player.getId()
                            sock.sendall(dumps(msg).encode())
                        self._started = True
                    else:
                        raise ValueError()

                except ValueError:
                    conn.sendall('1'.encode())

    """
        Message Sending Methods
    """

    def send_turn(self, player: Player) -> None:
        # Constructs and sends a TURN message
        msg = self._generate_message('TURN', player=player.getId())
        self._send_to_all(msg)

    def send_roll(self, player: Player, dice: list) -> None:
        msg = self._generate_message('ROLL', roll=dice)
        sock = self._player_sockets[player]
        sock.sendall(msg.encode())

    def send_buy_request(self, player: Player) -> None:
        msg = self._generate_message('BUY?')
        sock = self._player_sockets[player]
        sock.sendall(msg.encode())

    def send_bought(self, player: Player, tile: int) -> None:
        msg = self._generate_message('BOUGHT', player=player.getId(), tile=tile)
        self._send_to_all(msg)

    def send_sold(self, player: Player, tiles: list) -> None:
        msg = self._generate_message('SOLD', player=player.getId(), tiles=tiles)
        self._send_to_all(msg)

    def send_goto(self, player: Player, tile: int) -> None:
        # Constructs and sends a GOTO message
        msg = self._generate_message('GOTO', player=player.getId(), tile=tile)
        self._send_to_all(msg)

    def send_jailed(self, player: Player) -> None:
        """
        Informs all clients that a player has been sent to or freed from jail
        :param player: The player who is entering or leaving jail
        """
        msg = self._generate_message('JAIL', player=player.getId())
        self._send_to_all(msg)

    def send_pay(self, amount: int, player_from: Player or None=None, player_to: Player or None=None) -> None:
        # Constructs and sends a PAY message
        try:
            if player_from is None and player_to is None:
                raise ValueError()
            msg = self._generate_message(
                'PAY',
                amount=amount,
                player_from=player_from.getId(),
                player_to=player_to.getId())
            self._send_to_all(msg)
        except Exception as e:
            print(e)

    def send_card(self, card: Card) -> None:
        # Constructs and sends a CARD message
        msg = self._generate_message('CARD', text=card.getText(), is_bail=card.isBail())
        self._send_to_all(msg)

    def send_quit(self, player: Player) -> None:
        msg = self._generate_message('QUIT', player=player.getId())
        self._send_to_all(msg)

    def send_event(self, event_message: str) -> None:
        # Sends an event message through the CHAT feature
        self.send_chat(None, event_message)

    def send_chat(self, player: Player or None, message: str) -> None:
        # Send a chat message from 'player'
        msg = self._generate_message('CHAT', player=player, text=message)
        self._send_to_all(msg)

    def _send_to_all(self, msg: str) -> None:
        # Sends 'message' to all players in game
        for sock in self._socket_owners:
            msg = msg.encode()
            sock.sendall(msg)

    @staticmethod
    def _generate_message(command: str, **values: dict) -> str:
        # Returns a message dumped with the passed command and values
        return dumps(
            {
                'command': command,
                'values': values
            }
        )