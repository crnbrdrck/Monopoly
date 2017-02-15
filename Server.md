---
title: Server
---

# Server
*This class will be used to receive messages from the Client, and inform the Board of what is received*

## Ports in Use
- 44469 - Main Game Port: Clients will TCP connect to this port
- 44470 - Polling Port: Clients will `POLL` for servers using this port

## State
The Server will have the following pieces of state:

1. Map of player_ids to socket objects
    - This is to allow the Board to send messages based solely on player_id alone

2. An instance of the Board class
    - This is what will actually run the game.
    - The Server will receive and parse messages from Clients and call appropriate methods in the Board for game state updates
    
## Methods
The Server will have the following methods to be used by Board:

1. `send_goto(int player_id, int tile)`
    - Constructs and sends a `GOTO` message

2. `send_pay(int amount, int from=None, int to=None)`
    - Constructs and sends a `PAY` message
    - If _from_ or _to_ is `None`, the money is coming from the Bank
    - If one is None, the other must have a value

3. `send_card(Card card)`
    - Constructs and sends a `CARD` message
    
4. `send_turn(int player)`
    - Constructs and sends a `TURN` message
    
5. `send_event(str event_text)`
    - Sends a chat message to all players informing players of an event

## Required Methods
The Server will need the following methods to be in the Board class:

1. `handle_roll(int player)`
    - Informs the Board of a `ROLL` request from the Player _player_
    
2. `handle_buy(int player)`
    - Informs the Board of a `BUY` request from the Player _player_
    
3. `handle_sell(int player, int[] properties)`
    - Informs the Board of a `SELL` request from the Player _player_
    
4. `get_username(int player_id)`
    - Requests the username of the player with the id _player_id_
