import random
import otherTile
import Prop
import Card
import Player

#Test

class Board:
    def __init__ (self, server):
        self.server = server
        self.__players = []
        self.__currentTurn = None
        self.__winner = None
        self.__freeParking = 0
        self.currentTurn = None


    def initialise_board(self):
        Go = otherTile("go")
        CCGHC = Prop("Cork City Gaol Heritage Centre", 60)
        CC1 = Card("Community Chest")
        MH = Prop("Mizen Head", 60)
        IT = otherTile("Income tax")
        KS = Prop("Kent Station", 200)
        COP = Prop("Cork Opera House", 100)
        C1 = Card("Chance")
        THV = Prop("Trabolgan Holiday Vilage", 100)
        TEH = Prop("The English Market", 120)
        Jail = otherTile("jail")
        CRM = Prop("Cork Racecourse Mallow", 140)
        EC = Prop("Electric Company", 150)
        KGC = Prop("Kinsale Golf Course", 140)
        MR = Prop ("Munster Rugby", 160)
        PPBS = Prop("Parnell Place Bus Station", 200)
        SPS = Prop("St Patrick Street", 180)
        CC2 = Card("Community Chest")
        OL = Prop("Opera Lane", 180)
        MQSC = Prop("Merchants Quay Shopping Centre", 200)
        FP = otherTile("Free Parking")
        BC = Prop("Blackrock Castle", 220)
        C2 = Card("Chance")
        IE = Prop("Irish Examiner", 220)
        FWP = Prop("Fota Wildlife Park", 240)
        CA = Prop("Cork Airport", 200)
        CBM = Prop("Cork Butter Museum", 260)
        CH = Prop("City Hall", 260)
        UCC = Prop("University College Cork", 280)
        GTJ = otherTile("Go to jail")
        JVC = Prop("Jameson Visitor Centre", 300)
        FH = Prop("Fota House", 300)
        CC3 = Card("Community Chest")
        CHC = Prop("Cobh Heritage Centre", 320)
        POC = Prop ("Port of Cork", 200)
        C3 = Card("Chance")
        SB = Prop("Shandon Bells", 350)
        BD = otherTile("Bank Deposit")
        BC = Prop("Blarney Castle", 400)
        Properties = [Go, CCGHC, CC1, MH, IT, KS, COP, C1, THV, TEH, Jail, CRM,
        EC, KGC, MR, PPBS, SPS, CC2, OL, MQSC, FP, BC, C2, IE, FWP, CA, CA, CBM,
        CH, UCC, GTJ, JVC, FH, CC3, CHC, POC, C3, SB, BD, BC]

    def add_player(self, player):
        self.__players.append(player)



    def start(self):
        self.current_turn = players[0]
        self.server.send_turn(current_turn)


    def handle_roll(self, player):
        dice1 = randint(1, 6)
        dice2 = randint(1, 6)
        result = dice1 + dice2
        self.server.send_roll(player, dice1, dice2)
        playerMove(player, result)


    def end_turn(self, p):
        if p.getBankBal < 0:
            self.__players.remove(p)
            self.server.send_event("Player %s, is bankrupt and was removed from the game" % p.getUsername())

            owns = p.ownedProperties()
            self.server.send_sold(owns)
            self.server.handle_sell(p, own)
            for prop in owns:
                prop.setUnOwned()
        if len(players) == 1:
            winner = players[0]
            self.server.send_event("Player %s won the game with %i in there bank account, game over!" % winner.getUsername(), winner.getBankBal())
        self.currentTurn += 1
        if self.current_turn == len(players):
            self.current_turn = players[0]



    def playerMove(self, player, dice):
        player.movePosition(self.handle_roll(player))
        if player.getPos() > 39:
            #player has passed g0
            player.updateBank(200)
            self.server.send_pay(200, None, player)
            pos = player.getPos()
            pos = pos % 40
            player.movePosition(pos)
            self.server.got(player, pos)

        elif player.getPos == 30:
            player.goToJail()
            player.movePosition(10)
            self.server.got(player, 10)
            if player.hasJailCard():
                player.useJailCard()
            elif player.getJailCount() > 3:
                player.getOutOfJail()
                player.resetJailCount()
            else:
                player.updateJailCount()
        elif player.getPos() in [2,7,17,22,33,36]:
            if player.getPos() in [2, 17, 33]:
                return 0
            elif players.getPos() in [7,22,36]:
                return 0
        elif player.getPos() == 4 or 38:
            player.updateBank(-200)
            self.server.send_event()
            self.__freeParking += 200
        elif player.getPos() ==  20:
            player.updateBank(self.__freeParking)
            self.__freeParking = 0
        else:
            current_pos = player.getPos()
            prop = Properties[current_pos]
            if prop.isOwned():
                rent = prop.getRen()
                owner = prop.getOwner()
                for o in self.__players:
                    if owner == o.getUsername():
                        o.updateBank(rent)
                        player.updateBank(rent * -1)
                        self.server.send_pay(rent, player, o )
            elif not prop.isOwned():
                self.server.send_buy_request()

        def handle_buy(self, player):
            pos = player.getPos()
            prop = Properties[pos]
            prop.setOwner(player)
            player.addOwnProp(prop)
            amount = prop.getPrice()
            self.server.send_pay(amount, None, player)
            player.updateBank(amount * -1)
