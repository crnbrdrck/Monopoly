import pygame

class Player:
    _COLOURS = [(255,0,0),(0,0,255),(0,255,0),(255,128,0),(255,0,255),(0,0,0),(255,255,0),(0,255,255)]
    _NUM = 0
    '''
    surface = display surface
    colour = colour of player square
    num = player number
    board = board object
    '''
    def __init__(self, surface, board, username):
        self.tile = 0
        self.username = username
        self.money = 1500
        self.num = Player._NUM
        Player._NUM += 1
        self.board = board
        self.surface = surface
        self.colour = Player._COLOURS[self.num]
        self.coords = self.board.get_tileslot(0,self.num)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],10,10)
        pygame.draw.rect(surface,self.colour,self.rect)
        self.myfont = pygame.font.SysFont("Calibri", 17)
        self.text = "" + str(self.username) + " = $" + str(self.money)
        self.mytext = self.myfont.render(self.text, 1, self.colour)
        self.surface.blit(self.mytext,(635,(60+(self.num * 20))))
        self.injail = False
        self.properties = []
        self.hasBail = False

    # Draws a white square at previous location
    # Redraws player at new location
    def moveTo(self,tile):
        # Ensure tile is on board
        tile %= 40
        whiterect = pygame.Rect(self.coords[0],self.coords[1],10,10)
        pygame.draw.rect(self.surface,(255,255,255),whiterect)
        self.coords = self.board.get_tileslot(tile,self.num)
        self.rect = pygame.Rect(self.coords[0], self.coords[1], 10, 10)
        pygame.draw.rect(self.surface, self.colour, self.rect)

        # Update self.tile
        self.tile = tile

    def getCurrentTile(self):
        return self.tile

    def getUsername(self):
        return self.username

    def getmoney(self):
        return self.money

    def setMoney(self,value):
        self.money = value
        self.text = "" + str(self.username) + " = $" + str(self.money)
        self.mytext = self.myfont.render(self.text, 1, self.colour)
        whiterect = pygame.Rect(650,(60+(self.num*20)),120,17)
        pygame.draw.rect(self.surface,(255,255,255),whiterect)
        self.surface.blit(self.mytext, (635, (60 + (self.num * 20))))

    def inJail(self):
        return self.injail

    def movetoJail(self):
        player.moveTo(30)
        self.injail = True

    def free(self):
        self.injail = False

    def addproperty(self,tileno):
        if tileno not in self.properties:
            self.properties.append(tileno)

    def removeproperty(self,tileno):
        self.properties.remove(tileno)

    def getproperties(self):
        return self.properties

    def removeplayer(self):
        whiterect = pygame.Rect(self.coords[0], self.coords[1], 10, 10)
        pygame.draw.rect(self.surface, (255, 255, 255), whiterect)
        whiterect = pygame.Rect(650, (60 + (self.num * 20)), 120, 17)
        pygame.draw.rect(self.surface, (255, 255, 255), whiterect)

    def getBail(self):
        self.hasBail = True

    def useBail(self):
        self.hasBail = False