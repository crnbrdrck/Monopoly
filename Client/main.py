import sys

import pygame
import os
import random
from pygame.locals import *
from sys import exit

try:
    from .Client import Client
except SystemError:
    print("Monopoly.Client [ERROR]: Client must be run as a module. Check the README for instructions")
    exit(1)
# Assume other local imports pass
from .Board import Board
from .Button import Button
from .ChatWindow import ChatWindow
from .Player import Player


class Main:

    def __init__(self):
        self.turn = 0
        self.myturn = False
        self.playerid = None
        self.started = False
        # Can change playerlist to a dictionary if needed
        self.playerlist = {}
        self.client = Client(self)
        self.chat = ChatWindow(500, 720, self.client.chat)
        self.can_roll = False
        self.can_buy = False
        self.current_doubles = 0

    def init_display(self):
        self.chat.start()
        pygame.init()
        self.DISPLAYSURF = pygame.display.set_mode((1060, 720))
        pygame.display.set_caption("Monopoly")
        self.DISPLAYSURF.fill((255,255,255))
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (10, 20), (10, 700), 5)
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (10, 700), (790, 700), 5)
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (790, 700), (790, 20), 5)
        pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (790, 20), (10, 20), 5)
        if 'board.jpg' not in os.listdir('.'):
            os.chdir('Client')
        boardimg = pygame.image.load('board.jpg')
        boardx = 30
        boardy = 30
        self.DISPLAYSURF.blit(boardimg, (boardx, boardy))
        self.buy = Button(self.DISPLAYSURF, 820, 200, 120, 60, "Buy")
        self.sell = Button(self.DISPLAYSURF, 820, 120, 120, 60, "Sell")
        self.roll = Button(self.DISPLAYSURF, 820, 40, 120, 60, "Roll")
        self.endturn = Button(self.DISPLAYSURF, 820, 280, 120, 60, "End turn")
        self.showproperties = Button(self.DISPLAYSURF,820,360,120,60,"Properties")
        self.startbutton = Button(self.DISPLAYSURF,820,550,120,60,"Start")
        self.myfont = pygame.font.SysFont("Calibri", 20)
        self.board = Board()
        self.turntext = "Turn: Player " + str(self.turn) # Change to username later
        turntexrendered = self.myfont.render(self.turntext, 1, (0, 0, 0))
        self.DISPLAYSURF.blit(turntexrendered, (820, 15))

    def startgame(self, players, local):
        self.started = True
        for playerid in players:
            self.createplayer(int(playerid), players[playerid])
        self.playerid = local

    def receiveRoll(self, dice):
        # returns tuple containing the results of two dice rolls
        if dice[0] != dice[1]:
            self.can_roll = False
        else:
            self.current_doubles += 1

        if self.current_doubles == 3:
            self.can_roll = False

    def setmoney(self, playernum, value):
        player = self.playerlist[playernum]
        player.setMoney(value)

    def receiveID(self, playerid):
        self.playerid = playerid

    def createplayer(self, id, username):
        player = Player(self.DISPLAYSURF, self.board, username)
        self.playerlist[id] = player

    def receiveturn(self,playerid):
        # receive turn from server
        self.turn = playerid
        whiterect = pygame.Rect(820, 15, 200, 20)
        pygame.draw.rect(self.DISPLAYSURF, (255, 255, 255), whiterect)
        self.turntext = "Turn: Player " + str(playerid)
        turntexrendered = self.myfont.render(self.turntext, 1, (0, 0, 0))
        self.DISPLAYSURF.blit(turntexrendered, (820, 15))
        if self.playerid == playerid:
            self.myturn = True
            self.can_roll = True
            self.current_doubles = 0

    def buying(self):
        # server asks player if it wants to buy
        msg = "Would you like to buy this property? Click BUY to buy or ROLL/END to continue"
        self.chat.receive_chat(msg)
        self.can_buy = True

    # TODO - Handle doubles

    def bought(self, playerid, tile):
        self.playerlist[playerid].addproperty(tile)
        self.board.gettile(tile).setowner(self.playerlist[playerid].getUsername())

    def sold(self, playerid, tiles, owner=None):
        for tile in tiles:
            self.playerlist[playerid].removeproperty(tile)
            self.board.gettile(tile).setowner(owner)

    def moveplayer(self, playerid, tile):
        self.playerlist[playerid].moveTo(tile)

    def jail(self, playerid):
        if self.playerlist[playerid].inJail():
            #say hes out of jail
            # self.chat.send_chat("Player %s has left jail" % (self.playerlist[playerid]))
            self.playerlist[playerid].free()
        else:
            self.playerlist[playerid].movetoJail()
            #say hes in jail
            # self.chat.send_chat("Player %s has been put to jail" % (self.playerlist[playerid]))

    def pay(self, playerfrom, playerto, amount):
        pfrom = self.playerlist[playerfrom]
        current = pfrom.getmoney() - amount
        pfrom.setMoney(current)
        if playerto is not None:
            pto = self.playerlist[playerto]
            current = pto.getmoney() + amount
            pto.setMoney(current)

    def receivecard(self, text, is_bail=False):
        # self.chat.send_chat("You have received a card: " % text)
        if is_bail:
            self.playerlist[self.playerid].getBail()

    def displaychat(self, player, text):
        self.chat.receive_chat(text, player)

    def hasquit(self, playerid):
        player = self.playerlist[playerid]
        self.chat.send_chat("Player %s has quit" % (player.getUsername()))
        #change display to remove player
        player.removeplayer()

    def gameover(self):
        self.chat.send_chat("Game over!")
        text = "Game over!"
        font = pygame.font.SysFont("Calibri",90)
        renderedtext = font.render(text,1,(0,0,0))
        self.DISPLAYSURF.blit(renderedtext,(115,300))

    def displaytile(self, tile):
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

    def gettile(self, tileno):
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
                    if self.myturn:
                        if self.buy.pressed(pygame.mouse.get_pos()):
                            # Buy func goes here
                            if self.can_buy:
                                self.client.buy(True)
                                self.can_buy = False
                            else:
                                self.chat.receive_chat("You cannot BUY anything right now")
                        elif self.sell.pressed(pygame.mouse.get_pos()):
                            # Sell func goes here
                            print("Not Implemented")
                        elif self.roll.pressed(pygame.mouse.get_pos()):
                            if self.can_roll:
                                self.can_buy = False
                                self.client.roll()
                            else:
                                self.chat.receive_chat("You cannot roll anymore. Please END your turn")
                        elif self.endturn.pressed(pygame.mouse.get_pos()):
                            if self.can_roll:
                                self.chat.receive_chat("You can still roll. Please ROLL")
                            else:
                                self.client.endTurn()
                                self.can_buy = False
                                self.myturn = False
                    else:
                        self.chat.receive_chat("It's not your turn!")
                    if self.showproperties.pressed(pygame.mouse.get_pos()):
                        #sample
                        self.playerid = 0
                        self.createplayer(0,"Mutombo")
                        self.bought(0,27)
                        self.bought(0,34)
                        player = self.playerlist[self.playerid]
                        self.chat.send_chat("You own these properties:")
                        for property in player.getproperties():
                            self.chat.send_chat("%s" % (self.gettile(property).toString()))
                    elif self.startbutton.pressed(pygame.mouse.get_pos()):
                        if not self.started:
                            self.client.start()
                    for tile in self.board.gettiles():
                        if tile.pressed(pygame.mouse.get_pos()):
                            self.displaytile(tile)

            pygame.display.update()

    def create(self, host, username, password=None):
        self.client.create(host, username, password)

    def join(self, host, username, password=None):
        self.client.join(host, username, password)

    def poll(self):
        return Client.poll()

if __name__ == "__main__":
    main = Main()
    main.run()