import Tile

class Board:

    def __init__(self):
        self.tilelist = [None] * 40
        self.tilelist[0] = Tile.Tile(0,550,550,75,75)
        self.tilelist[1] = Tile.Tile(1,502, 565, 44, 60)
        self.tilelist[2] = Tile.Tile(2,455, 565, 44, 60)
        self.tilelist[3] = Tile.Tile(3,406, 565, 44, 60)
        self.tilelist[4] = Tile.Tile(4,357, 565, 44, 60)
        self.tilelist[5] = Tile.Tile(5,310, 565, 44, 60)
        self.tilelist[6] = Tile.Tile(6,261, 565, 44, 60)
        self.tilelist[7] = Tile.Tile(7,214, 565, 44, 60)
        self.tilelist[8] = Tile.Tile(8,164, 565, 44, 60)
        self.tilelist[9] = Tile.Tile(9,119, 565, 44, 60)
        self.tilelist[10] = Tile.Tile(10,35, 548, 75, 75)
        self.tilelist[11] = Tile.Tile(11,35, 500, 60, 40)
        self.tilelist[12] = Tile.Tile(12,35, 450, 60, 40)
        self.tilelist[13] = Tile.Tile(13,35, 404, 60, 40)
        self.tilelist[14] = Tile.Tile(14,35, 355, 60, 40)
        self.tilelist[15] = Tile.Tile(15,35, 310, 60, 40)
        self.tilelist[16] = Tile.Tile(16,35, 257, 60, 40)
        self.tilelist[17] = Tile.Tile(17,35, 210, 60, 40)
        self.tilelist[18] = Tile.Tile(18,35, 162, 60, 40)
        self.tilelist[19] = Tile.Tile(19,35, 115, 60, 40)
        self.tilelist[20] = Tile.Tile(20,35, 35, 75, 75)
        self.tilelist[21] = Tile.Tile(21,116, 35, 44, 60)
        self.tilelist[22] = Tile.Tile(22,164, 35, 44, 60)
        self.tilelist[23] = Tile.Tile(23,212, 35, 44, 60)
        self.tilelist[24] = Tile.Tile(24,261, 35, 44, 60)
        self.tilelist[25] = Tile.Tile(25,310, 35, 44, 60)
        self.tilelist[26] = Tile.Tile(26,358, 35, 44, 60)
        self.tilelist[27] = Tile.Tile(27,405, 35, 44, 60)
        self.tilelist[28] = Tile.Tile(28,455, 35, 44, 60)
        self.tilelist[29] = Tile.Tile(29,502, 35, 44, 60)
        self.tilelist[30] = Tile.Tile(30,550, 35, 75, 75)
        self.tilelist[31] = Tile.Tile(31,568, 115, 60, 40)
        self.tilelist[32] = Tile.Tile(32,568, 163, 60, 40)
        self.tilelist[33] = Tile.Tile(33,568, 209, 60, 40)
        self.tilelist[34] = Tile.Tile(34,568, 258, 60, 40)
        self.tilelist[35] = Tile.Tile(35,568, 308, 60, 40)
        self.tilelist[36] = Tile.Tile(36,568, 355, 60, 40)
        self.tilelist[37] = Tile.Tile(37,568, 404, 60, 40)
        self.tilelist[38] = Tile.Tile(38,568, 452, 60, 40)
        self.tilelist[39] = Tile.Tile(39,568, 500, 60, 40)

    def get_tileslot(self,tilenum,playernum):
        return self.tilelist[tilenum].get_slot(playernum)

    def gettiles(self):
        return self.tilelist