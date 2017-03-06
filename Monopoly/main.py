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
        self.turn = 0
        self.myturn = False
        self.playerid = None
        self.started = False
        # Can change playerlist to a dictionary if needed
        self.playerlist = []
        self.client = object()
        self.chat = ChatWindow.ChatWindow(500,720)
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((1060,720))
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
        self.showproperties = Button.Button(self.DISPLAYSURF,820,360,120,60,"Properties")
        self.startbutton = Button.Button(self.DISPLAYSURF,820,550,120,60,"Start")
        self.myfont = pygame.font.SysFont("Calibri", 20)
        self.board = Board.Board()
        self.turntext = "Turn: Player " + str(self.turn) # Change to username later
        turntexrendered = self.myfont.render(self.turntext, 1, (0, 0, 0))
        self.DISPLAYSURF.blit(turntexrendered, (820, 15))
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
        #if self.myturn:
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
        if dice[0] != dice[1]:
            self.myturn = False

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
        #self.turn = playerid
        #whiterect = pygame.Rect(820, 15, 200, 20)
        #pygame.draw.rect(self.DISPLAYSURF, (255, 255, 255), whiterect)
        #self.turntext = "Turn: Player " + str(playerid)
        #turntexrendered = self.myfont.render(self.turntext, 1, (0, 0, 0))
        #self.DISPLAYSURF.blit(turntexrendered, (820, 15))
        #if self.playerid == playerid:
            #self.myturn = True

    #def buying(self):
        # server asks player if it wants to buy

    def bought(self,playerid,tile):
        self.playerlist[playerid].addproperty(tile)
        self.board.gettile(tile).setowner(self.playerlist[playerid].getUsername())

    def sold(self,playerid,tiles,owner = "None"):
        for tile in tiles:
            self.playerlist[playerid].removeproperty(tile)
            self.board.gettile(tile).setowner = owner

    def moveplayer(self,playerid,tile):
        self.playerlist[playerid].moveTo(tile)

    def jail(self,playerid):
        if self.playerlist[playerid].inJail():
            #say hes out of jail
            self.playerlist[playerid].free()
        else:
            self.playerlist[playerid].movetoJail()
            #say hes in jail

    def pay(self,playerfrom,amount,playerto = "Bank"):
        pfrom = self.playerlist[playerfrom]
        current = pfrom.getmoney() - amount
        pfrom.setMoney(current)
        if playerto != "Bank":
            pto = self.playerlist[playerto]
            current = pto.getmoney() + amount
            pto.setMoney(current)

    def hasquit(self,playerid):
        player = self.playerlist[playerid]
        self.chat.send_chat("Player %s has quit" % (player.getUsername()))

    def displaytile(self,tile):
        whiterect = pygame.Rect(800, 450, 300, 80)
        pygame.draw.rect(self.DISPLAYSURF, (255, 255, 255), whiterect)
        text1 = "Tile selected: "
        text2 = tile.toString()
        text3 = "Owner: " + tile.getowner()
        mytext1 = self.myfont.render(text1, 1, (0, 0, 0))
        mytext2 = self.myfont.render(text2,1,(0,0,0))
        mytext3 = self.myfont.render(text3,1,(0,0,0))
        self.DISPLAYSURF.blit(mytext1, (800,450))
        self.DISPLAYSURF.blit(mytext2,(800,475))
        self.DISPLAYSURF.blit(mytext3,(800,500))

    def gettile(self,tileno):
        return self.board.gettile(tileno)

    def run(self):
        while True:
            if self.started:
                whiterect = pygame.Rect(820, 550, 120, 60)
                pygame.draw.rect(self.DISPLAYSURF, (255, 255, 255), whiterect)
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
                    elif self.endturn.pressed(pygame.mouse.get_pos()):
                        print("End Turn")
                    elif self.showproperties.pressed(pygame.mouse.get_pos()):
                        #sample
                        self.playerid = 0
                        self.createplayer((0,0,0),0,"Mutombo")
                        self.bought(0,27)
                        self.bought(0,34)
                        player = self.playerlist[self.playerid]
                        self.chat.send_chat("You own these properties:")
                        for property in player.getproperties():
                            self.chat.send_chat("%s" % (self.gettile(property).toString()))
                    elif self.startbutton.pressed(pygame.mouse.get_pos()):
                        if not self.started:
                            self.started = True
                            print("Start")
                    for tile in self.board.gettiles():
                        if tile.pressed(pygame.mouse.get_pos()):
                            self.displaytile(tile)

            pygame.display.update()

if __name__ == "__main__":
    main = Main()
    main.run()