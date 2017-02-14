# Server
*This class will be used to receive messages from the Client, and inform the Board of what is received*

## State
The Server will have the following pieces of state:

1. Map of player_ids to addresses
    - This is to allow the Board to send messages based solely on player_id alone

2. An instance of the Board class
    - This is what will actually run the game.
    - The Server will receive and parse messages from Clients and call appropriate methods in the Board for game state updates
    
## Methods
The Server will also have the following methods:

1. `send_goto(int player_id, int tile)`
    - Constructs and sends a `GOTO` message

2. `send_pay(int from, int to, int amount)`
    - Constructs and sends a `PAY` message

3. `send_card(Card card)`
    - Constructs and sends a `CARD` message
