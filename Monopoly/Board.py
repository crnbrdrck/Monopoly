import Tile

class Board:

    def __init__(self):
        self.tilelist = [None] * 40
        self.tilelist[0] = Tile.Tile("Go",554,550,75,75)
        self.tilelist[1] = Tile.Tile("Cork City Gaol Heritage Center",507, 568, 44, 60)
        self.tilelist[2] = Tile.Tile("Community Chest",458, 565, 44, 60)
        self.tilelist[3] = Tile.Tile("Mizen Head",408, 569, 44, 60)
        self.tilelist[4] = Tile.Tile("Income Tax",359, 565, 44, 60)
        self.tilelist[5] = Tile.Tile("Kent Station",310, 565, 44, 60)
        self.tilelist[6] = Tile.Tile("Cork Opera House",266, 569, 44, 60)
        self.tilelist[7] = Tile.Tile("Chance",214, 565, 44, 60)
        self.tilelist[8] = Tile.Tile("Trabolgan Holiday Village",168, 568, 44, 60)
        self.tilelist[9] = Tile.Tile("The English Market",119, 569, 44, 60)
        self.tilelist[10] = Tile.Tile("Jail",35, 552, 75, 75)
        self.tilelist[11] = Tile.Tile("Cork Racecourse Mallow",35, 503, 60, 40)
        self.tilelist[12] = Tile.Tile("Electric Company",35, 455, 60, 40)
        self.tilelist[13] = Tile.Tile("Kinsale Golf Course",35, 414, 60, 40)
        self.tilelist[14] = Tile.Tile("Munster Rugby",35, 361, 60, 40)
        self.tilelist[15] = Tile.Tile("Parnell Place Bus Station",35, 310, 60, 40)
        self.tilelist[16] = Tile.Tile("St Patrick Street",35, 263, 60, 40)
        self.tilelist[17] = Tile.Tile("Community Chest",35, 216, 60, 40)
        self.tilelist[18] = Tile.Tile("Opera Lane",35, 166, 60, 40)
        self.tilelist[19] = Tile.Tile("Merchants Quay",35, 115, 60, 40)
        self.tilelist[20] = Tile.Tile("Free Parking",35, 35, 75, 75)
        self.tilelist[21] = Tile.Tile("Blackrock Castle",120, 35, 44, 60)
        self.tilelist[22] = Tile.Tile("Chance",167, 35, 44, 60)
        self.tilelist[23] = Tile.Tile("Irish Examiner",216, 35, 44, 60)
        self.tilelist[24] = Tile.Tile("Fota Wildlife Park",264, 35, 44, 60)
        self.tilelist[25] = Tile.Tile("Cork Airport",310, 35, 44, 60)
        self.tilelist[26] = Tile.Tile("Cork Butter Museum",358, 35, 44, 60)
        self.tilelist[27] = Tile.Tile("City Hall",408, 35, 44, 60)
        self.tilelist[28] = Tile.Tile("The Lifetime Lab",455, 35, 44, 60)
        self.tilelist[29] = Tile.Tile("University College Cork",509, 35, 44, 60)
        self.tilelist[30] = Tile.Tile("Go to Jail",554, 35, 75, 75)
        self.tilelist[31] = Tile.Tile("Jameson Visitor Centre",570, 118, 60, 40)
        self.tilelist[32] = Tile.Tile("Fota House",570, 163, 60, 40)
        self.tilelist[33] = Tile.Tile("Community Chest",568, 214, 60, 40)
        self.tilelist[34] = Tile.Tile("Cobh Heritage Centre",572, 264, 60, 40)
        self.tilelist[35] = Tile.Tile("Port of Cork",568, 311, 60, 40)
        self.tilelist[36] = Tile.Tile("Chance",568, 359, 60, 40)
        self.tilelist[37] = Tile.Tile("Shandon Bells",570, 407, 60, 40)
        self.tilelist[38] = Tile.Tile("Bank Deposit",568, 455, 60, 40)
        self.tilelist[39] = Tile.Tile("Blarney Castle",570, 505, 60, 40)

    def get_tileslot(self,tilenum,playernum):
        return self.tilelist[tilenum].get_slot(playernum)

    def gettiles(self):
        return self.tilelist

    def gettile(self,tileno):
        return self.tilelist[tileno]