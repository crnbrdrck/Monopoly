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

1. An instance of the Board class
    - This is what will actually run the game.
    - The Server will receive and parse messages from Clients and call appropriate methods in the Board for game state updates
    
2. A map of addresses to Player objects
    - This is so the Server can pass Player object parameters to the Board
    - The socket will be stored in the Player class
    
## Methods
The Server will have the following methods to be used by Board:

1. `send_goto(Player player, int tile)`
    - Constructs and sends a `GOTO` message

2. `send_pay(int amount, Player from=None, Player to=None)`
    - Constructs and sends a `PAY` message
    - If _from_ or _to_ is `None`, the money is coming from the Bank
    - If one is None, the other must have a value

3. `send_card(Player player, Card card)`
    - Constructs and sends a `CARD` message
    
4. `send_turn(Player player)`
    - Constructs and sends a `TURN` message
    
5. `send_event(str event_text)`
    - Sends a chat message to all players informing players of an event
    
6. `send_roll(Player player, int dice1, int dice2)`
    - Constructs and sends a `ROLL` message

## Required Methods
The Server will need the following methods to be in the Board class:

1. `handle_roll(Player player)`
    - Informs the Board of a `ROLL` request from the Player _player_
    
2. `handle_buy(Player player)`
    - Informs the Board of a `BUY` request from the Player _player_
    
3. `handle_sell(Player player, int[] properties)`
    - Informs the Board of a `SELL` request from the Player _player_

4. `add_player(Player player)`
    - Add the Player _player_ to the board
