import random
import sys

import Board
import Button
import ChatWindow
import Player
import pygame
from pygame.locals import *

class Main():

	def __init__(self):
		self.playerlist = []
		self.client = object()
		self.chat = ChatWindow.ChatWindow(500, 720)
		pygame.init()
		self.DISPLAYSURF = pygame.display.set_mode((1024, 720))
		pygame.display.set_caption("Monopoly")
		self.DISPLAYSURF.fill((255, 255, 255))
		pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (10, 20), (10, 700), 5)
		pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (10, 700), (790, 700), 5)
		pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (790, 700), (790, 20), 5)
		pygame.draw.line(self.DISPLAYSURF, (0, 0, 0), (790, 20), (10, 20), 5)
		boardimg = pygame.image.load('board.jpg')
		boardx = 30
		boardy = 30
		self.DISPLAYSURF.blit(boardimg, (boardx, boardy))
		self.buy = Button.Button(DISPLAYSURF, 820, 200, 120, 60, "Buy")
		self.sell = Button.Button(DISPLAYSURF, 820, 120, 120, 60, "Sell")
		self.roll = Button.Button(DISPLAYSURF, 820, 40, 120, 60, "Roll")
		self.endturn = Button.Button(DISPLAYSURF, 820, 280, 120, 60, "End turn")
		self.board = Board.Board()

	def playerRoll(self,playernum):
		player = self.playerlist[playernum]
    	# Get the current tile of the player
    	tile = player.getCurrentTile()
    	# Roll two dice
    	dice = [random.randint(1, 6), random.randint(1, 6)]
    	# Send a chat message to say what happened
    	self.chat.send_chat('%s just rolled %i (%i, %i)' % (player.getUsername(), dice[0] + dice[1], dice[0], dice[1]))
    	player.moveTo(tile + dice[0] + dice[1])

    def setMoney(self,playernum,value):
    	player = self.playerlist[playernum]
    	player.setMoney(value)

	def createPlayer(self,colour,number,username)
		player = Player.Player(self.DISPLAYSURF,colour,number,self.board,username)
		self.playerlist.append(player)
			
if __name__ == "__main__":
	while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            chat.destroy()
            pygame.quit()
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            if self.buy.pressed(pygame.mouse.get_pos()):
                # Buy func goes here
                print("buy")
            elif self.sell.pressed(pygame.mouse.get_pos()):
                # Sell function goes here
                print("sell")
            elif self.roll.pressed(pygame.mouse.get_pos()):
                # Roll function goes here
                print("Roll")
            elif self.endturn.pressed(pygame.mouse.get_pos()):
                # End turn func goes here
                print("End turn")
    pygame.display.update()