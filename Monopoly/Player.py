import pygame

class Player:

    '''
    surface = display surface
    colour = colour of player square
    num = player number
    board = board object
    '''
    def __init__(self,surface,colour,num,board):
        self.num = num
        self.board = board
        self.surface = surface
        self.colour = colour
        self.coords = self.board.get_tileslot(0,self.num)
        self.rect = pygame.Rect(self.coords[0],self.coords[1],10,10)
        pygame.draw.rect(surface,colour,self.rect)

    #Draws a white square at previous location
    #Redraws player at new location
    def moveTo(self,tile):
        whiterect = pygame.Rect(self.coords[0],self.coords[1],10,10)
        pygame.draw.rect(self.surface,(255,255,255),whiterect)
        self.coords = self.board.get_tileslot(tile,self.num)
        self.rect = pygame.Rect(self.coords[0], self.coords[1], 10, 10)
        pygame.draw.rect(self.surface, self.colour, self.rect)