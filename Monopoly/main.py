import sys

import Board
import Button
import ChatWindow
import Player
import pygame
import os
from pygame.locals import *

class Main():

    def __init__(self):
        self.playerid = None
        # Can change playerlist to a dictionary if needed
        self.playerlist = []
        self.client = object()
        self.chat = ChatWindow.ChatWindow(500,720)
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((1024,720))
        pygame.display.set_caption("Monopoly")
        self.DISPLAYSURF.fill((255,255,255))
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (10, 20), (10, 700), 5)
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (10, 700), (790, 700), 5)
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (790, 700), (790, 20), 5)
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (790, 20), (10, 20), 5)
        if 'board.jpg' not in os.listdir():
            os.chdir('Monopoly')
        boardimg = pygame.image.load('board.jpg')
        boardx = 30
        boardy = 30
        self.DISPLAYSURF.blit(boardimg, (boardx, boardy))
        self.buy = Button.Button(self.DISPLAYSURF, 820, 200, 120, 60, "Buy")
        self.sell = Button.Button(self.DISPLAYSURF, 820, 120, 120, 60, "Sell")
        self.roll = Button.Button(self.DISPLAYSURF, 820, 40, 120, 60, "Roll")
        self.endturn = Button.Button(self.DISPLAYSURF, 820, 280, 120, 60, "End turn")
        self.board = Board.Board()

    """def playerroll(self,playernum):
        player = self.playerlist[playernum]
        # Get the current tile of the player
        tile = player.getCurrentTile()
        # Roll two dice
        dice = [random.randint(1, 6), random.randint(1, 6)]
        # Send a chat message to say what happened
        self.chat.send_chat('%s just rolled %i (%i, %i)' % (player.getUsername(), dice[0] + dice[1], dice[0], dice[1]))
        player.moveTo(tile + dice[0] + dice[1])"""

    #def roll(self):
    # inform server player wants to roll

    #def quit(self):
    # inform server player wants to quit

    #def start(self):
    # informs server player wants to start

    #def buy(self):
    # informs server player wants to buy

    #def sell(self):
    # informs server player wants to sell

    #def endturn(self):
    # informs server player wants to end turn

    def receiveRoll(self,playernum,dice):
        player = self.playerlist[playernum]
        self.chat.send_chat('%s just rolled %i (%i, %i)' % (player.getUsername(), dice[0] + dice[1], dice[0], dice[1]))
        player.moveTo(tile + dice[0] + dice[1])

    def setmoney(self,playernum,value):
        player = self.playerlist[playernum]
        player.setMoney(value)

    def receiveID(self,playerid):
        self.playerid = playerid

    def createplayer(self,colour,number,username):
        player = Player.Player(self.DISPLAYSURF, colour, number, self.board, username)
        self.playerlist.append(player)

    #def turn(self,playerid):
        # receive turn from server

    #def buying(self):
        # server asks player if it wants to buy

    #def bought(self,playerid,tile):
        # informs all clients player has bought tile

    #def sold(self,playerid,tiles):
        # informs all clients player has sold all properties in tiles

    def moveplayer(self,playerid,tile):
        self.playerlist[playerid].moveTo(tile)

    def jail(self,playerid):
        if self.playerlist[playerid].inJail():
            #say hes out of jail
            self.playerlist[playerid].free()
        else:
            self.playerlist[playerid].movetoJail()
            #say hes in jail

    #def pay(self,playerfrom,playerto,amount):
        # inform all clients player has from has paid amount to to

    #def hasquit(self,playerid):
        # inform all clients playernum has quit

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.chat.destroy()
                    pygame.quit()
                    sys.exit(0)
                elif event.type == MOUSEBUTTONDOWN:
                    if self.buy.pressed(pygame.mouse.get_pos()):
                        # Buy func goes here
                        print("Buy")
                    elif self.sell.pressed(pygame.mouse.get_pos()):
                        # Sell func goes here
                        print("Sell")
                    elif self.roll.pressed(pygame.mouse.get_pos()):
                        print("Roll")
            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.run()