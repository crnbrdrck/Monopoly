

class Tile:

    def __init__(self,x,y,width,height):
        self.slots = [None] * 8
        if width >= height :
            for i in range(4):
                self.slots[i] = (x +(i*(width/4)),y)
            for j in range(4):
                self.slots[j+4] = (x + (j*(width/4)),y + height / 2)
        else:
            for k in range(2):
                self.slots[k] = (x +(k*(width/2)),y)
            for l in range(2):
                self.slots[l+2] = (x +(l*(width /2)),y + (1*(height / 4)))
            for m in range(2):
                self.slots[m+4] = (x + (m*(width / 2)), y + (2*(height / 4)))
            for n in range(2):
                self.slots[n+6] = (x + (n*(width/2)),y + (3*(height/4)))

    def get_slot(self,playernum):
        return self.slots[playernum]