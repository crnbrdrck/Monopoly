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
- The Server will use the socket object obtained from accepting this connection to add to the map
- The _game_ value must be specified as Monopoly so the server will not accidentally be created for other games
- **Returns: Success / Fail**

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
- **Returns: GAME**

### Games
```python
{
    "command": "GAME",
    "values": {
        "game": game_details
    }
}
```
- This message is sent as a response to a `POLL` request
- The Client can use these messages to build up a list of currently open games on the network

### Join
```python
{
    "command": "JOIN",
    "values": {
        "username": str username,
        "password": str password or None
    }
}
```
- This will be sent to a server found using the POLL command
- **Returns: Success / Fail**

## Client-to-Server Commands
These commands are used to pass user input to the server to control the state of the game

### Roll
```python
{
    "command": "ROLL",
    "values": {}
}
```
- Instructs the server to roll a dice for the client that sends the request
- **Returns: ROLL**

### Buy
```python
{
    "command": "BUY",
    "values": {}
}
```
- Instructs the server to buy the property that the client is currently at
- Will be updated later to include support for houses / hotels
- **Returns: Success / Fail**

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
- **Returns: PAY**

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
## Server-to-Client Commands
These commands are used to inform clients of an update to the state

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
