# API

Our API between server and client is based on a simple JSON structure

```python
{
    "command": "COMMAND_NAME",
    "values": ["list", "of", "values"]
}
```

## Client-to-Server Commands
These commands are used to pass user input to the server to control the state of the game

### Roll
```python
{
    "command": "ROLL",
    "values": []
}
```
- Instructs the server to roll a dice for the client that sends the request


### Buy
```python
{
    "command": "BUY",
    "values": []
}
```
- Instructs the server to buy the property that the client is currently at
- Will be updated later to include support for houses / hotels


### Sell
```python
{
    "command": "SELL",
    "values": [int id1, int id2, int ..., int idn]
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
    "values": [int player_id, int tile]
}
```
- Instruct clients that the player _player_id_ has moved to _tile_


### Pay
```python
{
    "command": "PAY",
    "values": [int from_player, int to_player, int amount]
}
```
- Instructs clients that player _from_player_ has paid _amount_ to _to_player_


### Card
```python
{
    "command": "CARD",
    "values": [str card_text, bool bail_card]
}
```
- Sends the text of a Chance / Community Chest card that a client has landed on to the client
- The actual mechanism of the card will be handled by the server
- If _bail_card_ is True, then the client will be awarded a *Get out of jail free* card (maybe implement later?)
