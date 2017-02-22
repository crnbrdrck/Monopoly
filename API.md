---
title: API
---

# API

Our API between server and client is based on a simple JSON structure

```python
{
    "command": "COMMAND_NAME",
    "values": {
        "value_name": "value"
    }
}
```

*For port values used, see the [Server](Server "Server") documentation*

## Note: Success / Failure
When a message below says **Returns: Success / Failure**, expect the following:

- The string `'0'` in case of a success
- The string `'1'` in case of a failure

## Game Discovery Commands
These commands are used by Clients to find and join open games

### Create
```python
{
    "command": "CREATE",
    "values": {
        "game": "Monopoly",
        "username": str host_username,
        "password": str password or None
    }
}
```
- This will normally be sent to the _localhost_, but it allows for externally located servers also (later)
- If no password is used, _password_ will be None
- Else the password should be encrypted using the following: `sha256(password.encode()).hexdigest()`
- The Server will use the socket object obtained from accepting this connection to add to the map
- The _game_ value must be specified as Monopoly so the server will not accidentally be created for other games
- **Returns: [Success / Failure][1]**

### Poll
```python
{
    "command": "POLL",
    "values": {
        "game": "Monopoly"
    }
}
```
- This is used to discover any open games on the network.
- This is the only message that will be sent and received using UDP, since you cannot broadcast with TCP
- The value is important to determine that the correct game is being polled for
- **Returns: [GAME](#game) / Failure**

### Join
```python
{
    "command": "JOIN",
    "values": {
        "game": "Monopoly",
        "username": str username,
        "password": str password or None
    }
}
```
- This will be sent to a server found using the POLL command
- If no password is used, _password_ will be None
- Else the password should be encrypted using the following: `sha256(password.encode()).hexdigest()`
- **Returns: [Success / Failure][1]**

## Client-to-Server Commands
These commands are used to pass user input to the server to control the state of the game

### Start
```python
{
    "command": "START",
    "values": {}
}
```
- Instructs the server to start the game
- Only works if the host (id = 0) sends the message
- **Returns: [START](#start-1) / Failure**

### Roll
```python
{
    "command": "ROLL",
    "values": {}
}
```
- Instructs the server to roll a dice for the client that sends the request
- **Returns: [ROLL](#roll-1)**

### Buy
```python
{
    "command": "BUY",
    "values": {
        "buy": 0 or 1 for YES or NO
    }
}
```
- Replies to the Server's [BUY?](#buy-request) with whether they want to purchase the property they are on or not
- Will be updated later to include support for houses / hotels
- **Returns: [BOUGHT](#bought)**

### Sell
```python
{
    "command": "SELL",
    "values": {
        "ids": [int id1, int id2, ..., int idn]
    }
}
```
- Instruct the server to mortgage the properties identified by the ids _id1_ to _idn_
- Will be expanded later to include support for houses / hotels
- **Returns: [PAY](#pay)**

### Chat
```python
{
    "command": "CHAT",
    "values": {
        "text": str text
    }
}
```
- Instruct the Server to pass on a chat message to all clients
- The server will automatically attach things like the username of the sender
- **Returns: [CHAT](#chat-1)**

## Server-to-Client Commands
These commands are used to inform clients of an update to the state

### Game
```python
{
    "command": "GAME",
    "values": {
        "game": {
            "players": [str username for Player in game],
            "password": bool has_password
        }
    }
}
```
- This message is sent as a response to a `POLL` request
- The Client can use these messages to build up a list of currently open games on the network

### Start
```python
{
    "command": "START",
    "values": {}
}
```
- Sent in response to the host sending a `START` request
- Informs the Clients that the game has started

### Turn
```python
{
    "command": "TURN",
    "values": {
        "player": int player_id
    }
}
```
- Inform all the clients whose turn it is

### Roll
```python
{
    "command": "ROLL",
    "values": {
        "roll": [int dice, int dice]
    }
}
```
- Informs a Client of their Roll value when they send a roll request
- Sends both dice value to inform the Client if they got a double

### Buy Request
```python
{
    "command": "BUY?",
    "values": {}
}
```
- Asks the Player whose turn it is whether or not they'd like to buy the property they are standing on

### Bought
```python
{
    "command": "BOUGHT",
    "values": {
        "player": int player_id,
        "tile": int tile
    }
}
```
- Informs all clients that the Player _player_id_ bought the property at position _tile_

### Go To
```python
{
    "command": "GOTO",
    "values": {
        "player": int player_id,
        "tile": int tile
    }
}
```
- Instruct clients that the player _player_id_ has moved to _tile_

### Pay
```python
{
    "command": "PAY",
    "values": {
        "from": int player_id or None,
        "to": int player_id or None,
        "amount": int amount
    }
}
```
- Instructs clients that player _from_ has paid _amount_ to _to_
- Either _from_ or _to_ can be None, indicating a payment from / to the Bank
- Only one of these can be None in any one payload

### Card
```python
{
    "command": "CARD",
    "values": {
        "text": str text,
        "is_bail": bool is_bail
    }
}
```
- Sends the text of a Chance / Community Chest card that a client has landed on to the client
- The actual mechanism of the card will be handled by the server
- If _is_bail_ is True, then the client will be awarded a *Get out of jail free* card (maybe implement later?)

### Chat
```python
{
    "command": "CHAT",
    "values": {
        "player": str username or None,
        "text": str message
    }
}
```
- Sends a chat message to all players
- If _username_ is None, the message is directly from the server
- Else it is from the player named _username_

## Implementation
- We intend to have a method in our server to handle all of these messages in separate threads to keep the server running quickly.
- We will separate our communication and logic into a Server and Board class respectively.
- The Server will make use of methods in the Board to handle messages sent from Clients
- The Server will also have chat functionality built in, to be handled solely by the Server
- The Server can also use the chat functionality to inform the Players of events

[1]: #note-success--failure
