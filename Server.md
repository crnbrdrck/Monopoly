---
title: Server
---

# Server
*This class will be used to receive messages from the [Client](1), and inform the [Board](2) of what is received*

## Ports in Use
- 44469 - Main Game Port: Clients will TCP connect to this port
- 44470 - Polling Port: Clients will `POLL` for servers using this port

## State
The Server will have the following pieces of state:

1. An instance of the Board class
    - This is what will actually run the game.
    - The Server will receive and parse messages from [Client](1)s and call appropriate methods in the [Board](2) for game state updates
    
2. A map of Player objects to sockets
    - This allows the Server to send to [Player](3)s with just an instance of a [Player](3) object

3. A map of sockets to Player objects
    - This allows the Server to determine a [Player](3) by receiving a message from a socket
    
## Methods
The Server will have methods to provide the Board with the ability to send out every kind of message from the [Server-To-Client](https://crnbrdrck.github.io/Monopoly/API#server-to-client-commands) section of the [API](4).

As well as this, the Server will require methods in the [Board](2) class that can handle the messages in the [Client-To-Server](https://crnbrdrck.github.io/Monopoly/API#client-to-server-commands) section of the [API](4).

---

# Message Sending Method Signatures
```python
def send_turn(self, player: Player) -> None:
    pass

def send_roll(self, player: Player, dice: list) -> None:
    pass

def send_buy_request(self, player: Player) -> None:
    pass
    
def send_bought(self, player: Player, tile: int) -> None:
    pass

def send_sold(self, player: Player, tiles: list) -> None:
    pass

def send_goto(self, player: Player, tile: int) -> None:
    pass

def send_jailed(self, player: Player) -> None:
    pass

def send_pay(self, amount: int, player_from: Player or None=None, player_to: Player or None=None) -> None:
    pass

def send_card(self, card: Card) -> None:
    pass

def send_quit(self, player: Player) -> None:
    pass

def send_event(self, event_message: str) -> None:
    pass

def send_chat(self, player: Player or None, message: str) -> None:
    pass
```

_These methods are the ones that will be used by the Board to use the API to update clients_

[1]: https://crnbrdrck.github.io/Monopoly/Client
[2]: https://crnbrdrck.github.io/Monopoly/Board
[3]: https://crnbrdrck.github.io/Monopoly/Player
[4]: https://crnbrdrck.github.io/Monopoly/API
