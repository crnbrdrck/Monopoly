import pygame

class Player:

    '''
    surface = display surface
    colour = colour of player square
    num = player number
    board = board object
    '''
    def __init__(self,surface,colour,num,board):
        self.money = 1500
        self.num = num
        self.board = board
        self.surface = surface
        self.colour = colour
        self.coords = self.board.get_tileslot(0,self.num)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],10,10)
        pygame.draw.rect(surface,colour,self.rect)
        self.myfont = pygame.font.SysFont("Calibri", 17)
        self.text = "Player " + str(self.num) + " = $" + str(self.money)
        self.mytext = self.myfont.render(self.text, 1, (0, 0, 0))
        self.surface.blit(self.mytext,(650,(60+(self.num * 20))))

    # Draws a white square at previous location
    # Redraws player at new location
    def moveTo(self,tile):
        whiterect = pygame.Rect(self.coords[0],self.coords[1],10,10)
        pygame.draw.rect(self.surface,(255,255,255),whiterect)
        self.coords = self.board.get_tileslot(tile,self.num)
        self.rect = pygame.Rect(self.coords[0], self.coords[1], 10, 10)
        pygame.draw.rect(self.surface, self.colour, self.rect)

    # Draws a white square at previous text
    # Redraws text with new money value
    def setMoney(self,value):
        self.money = value
        self.text = "Player " + str(self.num) + " = $" + str(self.money)
        self.mytext = self.myfont.render(self.text, 1, (0, 0, 0))
        whiterect = pygame.Rect(650,(60+(self.num*20)),120,17)
        pygame.draw.rect(self.surface,(255,255,255),whiterect)
        self.surface.blit(self.mytext, (650, (60 + (self.num * 20))))