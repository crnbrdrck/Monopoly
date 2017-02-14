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


### Buy
```python
{
    "command": "BUY",
    "values": {}
}
```
- Instructs the server to buy the property that the client is currently at
- Will be updated later to include support for houses / hotels


### Sell
```python
{
    "command": "SELL",
    "values": {
        "ids": [int id1, int id2, ..., int idn]
    }
}
```
- Instruct the server to sell the properties identified by the ids _id1_ to _idn_
- Will be expanded later to include support for houses / hotels
    
## Server-to-Client Commands
These commands are used to inform clients of an update to the state


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
        "from": int player_id,
        "to": int player_id,
        "amount": int amount
    }
}
```
- Instructs clients that player _from_ has paid _amount_ to _to_


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

## Implementation
- We intend to have a method in our server to handle all of these messages in separate threads to keep the server running quickly.
- We will separate our communication and logic into a Server and Board class respectively.
- The Server will make use of methods in the Board to handle messages sent from Clients
- The Server will also have chat functionality built in, to be handled solely by the Server
