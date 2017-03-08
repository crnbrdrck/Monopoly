from .Tile import Tile

class Board:

    def __init__(self):
        self.tilelist = [None] * 40
        self.tilelist[0] = Tile("Go",554,550,75,75)
        self.tilelist[1] = Tile("Cork City Gaol Heritage Center",507, 568, 44, 60)
        self.tilelist[2] = Tile("Community Chest",458, 565, 44, 60)
        self.tilelist[3] = Tile("Mizen Head",408, 569, 44, 60)
        self.tilelist[4] = Tile("Income Tax",359, 565, 44, 60)
        self.tilelist[5] = Tile("Kent Station",310, 565, 44, 60)
        self.tilelist[6] = Tile("Cork Opera House",266, 569, 44, 60)
        self.tilelist[7] = Tile("Chance",214, 565, 44, 60)
        self.tilelist[8] = Tile("Trabolgan Holiday Village",168, 568, 44, 60)
        self.tilelist[9] = Tile("The English Market",119, 569, 44, 60)
        self.tilelist[10] = Tile("Jail",35, 552, 75, 75)
        self.tilelist[11] = Tile("Cork Racecourse Mallow",35, 503, 60, 40)
        self.tilelist[12] = Tile("Electric Company",35, 455, 60, 40)
        self.tilelist[13] = Tile("Kinsale Golf Course",35, 414, 60, 40)
        self.tilelist[14] = Tile("Munster Rugby",35, 361, 60, 40)
        self.tilelist[15] = Tile("Parnell Place Bus Station",35, 310, 60, 40)
        self.tilelist[16] = Tile("St Patrick Street",35, 263, 60, 40)
        self.tilelist[17] = Tile("Community Chest",35, 216, 60, 40)
        self.tilelist[18] = Tile("Opera Lane",35, 166, 60, 40)
        self.tilelist[19] = Tile("Merchants Quay",35, 115, 60, 40)
        self.tilelist[20] = Tile("Free Parking",35, 35, 75, 75)
        self.tilelist[21] = Tile("Blackrock Castle",120, 35, 44, 60)
        self.tilelist[22] = Tile("Chance",167, 35, 44, 60)
        self.tilelist[23] = Tile("Irish Examiner",216, 35, 44, 60)
        self.tilelist[24] = Tile("Fota Wildlife Park",264, 35, 44, 60)
        self.tilelist[25] = Tile("Cork Airport",310, 35, 44, 60)
        self.tilelist[26] = Tile("Cork Butter Museum",358, 35, 44, 60)
        self.tilelist[27] = Tile("City Hall",408, 35, 44, 60)
        self.tilelist[28] = Tile("The Lifetime Lab",455, 35, 44, 60)
        self.tilelist[29] = Tile("University College Cork",509, 35, 44, 60)
        self.tilelist[30] = Tile("Go to Jail",554, 35, 75, 75)
        self.tilelist[31] = Tile("Jameson Visitor Centre",570, 118, 60, 40)
        self.tilelist[32] = Tile("Fota House",570, 163, 60, 40)
        self.tilelist[33] = Tile("Community Chest",568, 214, 60, 40)
        self.tilelist[34] = Tile("Cobh Heritage Centre",572, 264, 60, 40)
        self.tilelist[35] = Tile("Port of Cork",568, 311, 60, 40)
        self.tilelist[36] = Tile("Chance",568, 359, 60, 40)
        self.tilelist[37] = Tile("Shandon Bells",570, 407, 60, 40)
        self.tilelist[38] = Tile("Bank Deposit",568, 455, 60, 40)
        self.tilelist[39] = Tile("Blarney Castle",570, 505, 60, 40)

    def get_tileslot(self,tilenum,playernum):
        return self.tilelist[tilenum].get_slot(playernum)

    def gettiles(self):
        return self.tilelist

    def gettile(self,tileno):
        return self.tilelist[tileno]