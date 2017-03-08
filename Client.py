import json
from select import select
from socket import *
from threading import Thread


class Client:

    def __init__(self, gui):
        self.sock = socket()
        self.gui = gui
        self.gameOver = False
        self.inGame = False

        
    def _sendCommand(self, command, **values):
        #command is a str e.g. "CREATE"
        #values is a dict e.g. {"game": "Monopoly}

        message = {"command" : command, "values": values}
        jsonMessage = json.dumps(message)
        self.sock.sendall(jsonMessage.encode())
        
    def _getReply(self):
        return sock.recv(4096).decode()


    """
    GAME DISCOVERY COMMANDS
    """

    def create(self, username, password = None, host):
        if not self.inGame:
            #str, str
            self.sock.connect((host, 44469))
            self._sendCommand("CREATE", game="Monopoly", username=username, password=password)
            res = self._getReply
            # 1 for SUCCESS, 0 for FAILURE
            if res == '0':
                # Invalid CREATE
                self.sock.close()
                self.sock = socket()
            else:
                self.inGame = True
      

    def poll(self):
        if not self.inGame:
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            timeouts = 3
            sock.settimeout(2)
            data = json.dumps({'command': 'POLL', 'values': {'game': 'Monopoly'}})
            sock.sendto(data.encode(), ('255.255.255.255', 44470))
            servers = {}
            while timeouts > 0:
                try:
                    data, address = sock.recvfrom(1024)
                    data = loads(data.decode())
                    server_address = address[0]
                    servers[server_address] = data['values']
                except timeout:
                    timeouts -= 1
            return servers


    def join(self, username, password = None, host):
        if not self.inGame:
            #str, str
            self.sock.connect((host, 44469))
            self._sendCommand("JOIN", **{"game": "Monopoly", "username": username, "password": password})
            res = self._getReply
            # 1 for SUCCESS, 0 for FAILURE
            if res == '0':
                # Invalid CREATE
                self.sock.close()
                self.sock = socket()
            else:
                self.inGame = True


    """
    CLIENT-TO-SERVER COMMANDS
    """

    def quit(self):
        self.gameOver = True
        self._sendCommand("QUIT")

    def start(self):
        self._sendCommand("START")
        res = self._getReply 
        # 1 for SUCCESS, 0 for FAILURE
        if res == '0':
            # Invalid CREATE
            
        else:
            self.gui.started(res)

    def roll(self):
        self._sendCommand("ROLL")

    def buy(self, yn):
        #int 0 for yes, 1 for no
        self._sendCommand("BUY", **{"buy": yn})

    def sell(self, tiles):
        #array of int tile numbers
        self._sendCommand("SELL", **{"tiles": tiles})

    def chat(self, text):
        #str
        self._sendCommand("CHAT", **{"text": text})

    def endTurn(self):
        self._sendCommand("END")

    def _listen(self):
        # Listen for messages from server and handle accordingly
        while not self.gameOver:
            connections, wlist, xlist = select([self.sock], [], [], 0.05)

            for conn in connections:
                data = conn.recv(4096).decode()
                try:
                    data = json.loads(data)
                    Thread(
                        target=self._handleMessage,
                        args=(data,),
                        daemon=True
                    ).start()
                except ValueError:
                    if message:
                        if len(message.split('}{')) == 1:
                            print("Invalid JSON string received: " + message)
                        else:
                            print("Combined JSON payloads received: " + message)
                            messages = message.split('}{')
                            messages[0] += '}'
                            messages[-1] = '{' + messages[-1]
                            for i, payload in enumerate(messages[1: -1], 1):
                                messages[i] = '{' + payload + '}'
                            for message in messages:
                                try:
                                    message = json.loads(message)
                                    Thread(
                                        target=self._handleMessage,
                                        args=(message,),
                                        daemon=True
                                    ).start()
                                except ValueError:
                                    print("Invalid JSON string received: " + message)
                except:
                    pass

    def _handleMessage(self, data):
        # Handle the data; parse command and call relevant function
        try:
            # Run through all the possible api commands and run the appropriate function
            if 'command' not in payload:
                raise ValueError()

            command = payload['command']

            if command == 'TURN':
                self.gui.turn = payload['values']['player']
            elif command == 'ROLL':
                #the gui method shouldnt need a playernum
                self.gui.receiveRoll(payload['values']['roll'])
            elif command == 'BUY?':
                self.gui.buying()
            elif command == 'BOUGHT':
                self.gui.bought(payload['values']['player'], payload['values']['tile'])
            elif command == 'SOLD':
                #None not "None"
                self.gui.sold(payload['values']['player'], payload['values']['tiles'])
            elif command == 'GOTO':
                self.gui.moveplayer(payload['values']['player'], payload['values']['tile'])
            elif command == 'JAIL':
                self.gui.jail(payload['values']['player'])
            elif command == 'PAY':
                #gui needs to change order of args
                #"Bank" should be None
                self.gui.pay(payload['values']['player_from'],
                             payload['values']['player_to'], payload['values']['amount'])
            elif command == 'CARD':
                #gui needs to handle card message
                self.gui.WHATEVER(payload['values']['text'], payload['values']['is_bail'])
            elif command == 'QUIT':
                #gui needs to do more e.g. take them off display
                self.gui.hasquit(payload['values']['player'])
            elif command == 'CHAT':
                #gui main needs method to handle chat
                self.gui.WHATEVER(payload['values']['player'], payload['values']['text'])
            elif command == 'GAMEOVER':
                #gui needs gameover method
                self.gui.gameover()
            else:
                raise ValueError()

        except (ValueError, KeyError):
            print("Invalid game command received: " + payload)
        
