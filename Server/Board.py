from random import randint
from .Card import Card
from .OtherTile import OtherTile
from .Prop import Prop

class Board:
    def __init__ (self, server):
        self.server = server
        self.__players = []
        self.__current_turn = 0
        self.__current_doubles = 0
        self.__winner = None
        self.__freeParking = 0
        self.__properties = []


    def initialise_board(self):
        self.__properties = [
            OtherTile("Go"),
            Prop("Cork City Gaol Heritage Centre", 60),
            Card("Community Chest"),
            Prop("Mizen Head", 60),
            OtherTile("Income Tax"),
            Prop("Kent Station", 200),
            Prop("Cork Opera House", 100),
            Card("Chance"),
            Prop("Trabolgan Holiday Vilage", 100),
            Prop("The English Market", 120),
            OtherTile("Jail"),
            Prop("Cork Racecourse Mallow", 140),
            Prop("Electric Company", 150),
            Prop("Kinsale Golf Course", 140),
            Prop ("Munster Rugby", 160),
            Prop("Parnell Place Bus Station", 200),
            Prop("St Patrick Street", 180),
            Card("Community Chest"),
            Prop("Opera Lane", 180),
            Prop("Merchants Quay Shopping Centre", 200),
            OtherTile("Free Parking"),
            Prop("Blackrock Castle", 220),
            Card("Chance"),
            Prop("Irish Examiner", 220),
            Prop("Fota Wildlife Park", 240),
            Prop("Cork Airport", 200),
            Prop("Cork Butter Museum", 260),
            Prop("City Hall", 260),
            Prop("The Lifetime Lab", 150),
            Prop("University College Cork", 280),
            OtherTile("Go To Jail"),
            Prop("Jameson Visitor Centre", 300),
            Prop("Fota House", 300),
            Card("Community Chest"),
            Prop("Cobh Heritage Centre", 320),
            Prop("Port of Cork", 200),
            Card("Chance"),
            Prop("Shandon Bells", 350),
            OtherTile("Bank Deposit"),
            Prop("Blarney Castle", 400)
        ]

    def add_player(self, player):
        self.__players.append(player)

    def game(self):
        for p in __players:
            if len(self.__players) > 1:
                self.server.send_turn(p)
                if p.getBankBal < 0:
                    self.__players.remove(p)
            else:
                self.__winner = p.getUsername

    def start(self):
        self.server.send_turn(self.__players[self.current_turn])

    def handle_roll(self, player):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        result = dice1 + dice2
        # Determine the situation for doubles
        if dice1 == dice2:
            # Are they already in jail?
            if player.getInJail():
                # They've been let out
                player.setInJail()
                self.server.send_jailed(player)
            else:
                self.__current_doubles += 1

        if self.__current_doubles >= 3:
            self.send_to_jail(player)
        else:
            self.server.send_roll(player, dice1, dice2)
            self.player_move(player, result)

    def handle_end(self, player):
        self.__current_doubles = 0
        if player.getBankBal < 0:
            self.__players.remove(player)
            self.server.send_event("Player %s, is bankrupt and was removed from the game" % player.getUsername())
            owns = player.ownedProperties()
            self.server.send_sold(player, owns)
            for prop in owns:
                prop.setUnOwned()

        if len(self.__players) == 1:
            winner = self.__players[0]
            self.server.send_event("Player %s won the game with %i in their bank account, game over!" % (
                winner.getUsername(), winner.getBankBal()))
        self.__current_turn = (self.__current_turn + 1 % len(self.__players))

    def player_move(self, player, dice):
        # Update player position
        player.movePosition(dice)
        pos = player.getPos()
        if pos > 39:
            # Player has passed go
            player.updateBank(200)
            self.server.send_pay(200, None, player)
            pos = player.getPos() % 40
            player.movePosition(pos)
            self.server.send_goto(player, pos)

        # Player landed on send to jail
        elif pos == 30:
            self.send_to_jail(player)

        # Player landed on a chance / community chest
        elif pos in [2, 7, 17, 22, 33, 36]:
            if pos in [2, 17, 33]:
                return 0
            elif pos in [7, 22, 36]:
                return 0

        # Player landed on tax
        elif pos in [4, 38]:
            player.updateBank(-200)
            self.server.send_pay(200, player, None)
            self.__freeParking += 200

        # Player landed on free parking
        elif pos == 20:
            player.updateBank(self.__freeParking)
            self.server.send_pay(self.__freeParking, None, player)
            self.__freeParking = 0

        # No special tile, normal property
        else:
            prop = self.__properties[pos]
            if prop.isOwned():
                owner = prop.getOwner()
                if owner != player:
                    rent = prop.getRent()
                    owner.updateBank(rent)
                    player.updateBank(rent * -1)
                    self.server.send_pay(rent, player, owner)
            else:
                self.server.send_buy_request()

    def send_to_jail(self, player):
        player.goToJail()
        player.movePosition(10)
        self.server.send_goto(player, 10)
        if player.hasJailCard():
            player.useJailCard()
        else:
            self.server.send_jailed(player)

    def handle_buy(self, player):
        pos = player.getPos()
        prop = self.__properties[pos]
        prop.setOwner(player)
        player.addOwnProp(prop)
        amount = prop.getPrice()
        self.server.send_pay(amount, player, None)
        player.updateBank(amount * -1)
