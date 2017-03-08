import random
import sys

import Board
import Button
import ChatWindow
import Player
import pygame
from pygame.locals import *

# Set up Client to send messages
client = object()

# Set up Chat Window
chat = ChatWindow.ChatWindow(500, 720)  #, client.send_chat)

pygame.init()

# Creating the display surface
DISPLAYSURF = pygame.display.set_mode((1024, 720))
pygame.display.set_caption("Monopoly")
DISPLAYSURF.fill((255, 255, 255))

# Drawing the black outline around the game
pygame.draw.line(DISPLAYSURF, (0, 0, 0), (10, 20), (10, 700), 5)
pygame.draw.line(DISPLAYSURF, (0, 0, 0), (10, 700), (790, 700), 5)
pygame.draw.line(DISPLAYSURF, (0, 0, 0), (790, 700), (790, 20), 5)
pygame.draw.line(DISPLAYSURF, (0, 0, 0), (790, 20), (10, 20), 5)

# Display image of board
boardimg = pygame.image.load('board.jpg')
boardx = 30
boardy = 30
DISPLAYSURF.blit(boardimg, (boardx, boardy))

# Make the buttons
buy = Button.Button(DISPLAYSURF, 820, 200, 120, 60, "Buy")
sell = Button.Button(DISPLAYSURF, 820, 120, 120, 60, "Sell")
roll = Button.Button(DISPLAYSURF, 820, 40, 120, 60, "Roll")
endturn = Button.Button(DISPLAYSURF, 820, 280, 120, 60, "End turn")

# Make the board
board = Board.Board()

# Make a player

player1 = Player.Player(DISPLAYSURF, (160,30,160), 0, board, "Player 1")
player2 = Player.Player(DISPLAYSURF, (30,30,30), 1, board, "Player 2")

# Sample buttons for player movement
move1 = Button.Button(DISPLAYSURF, 820, 360, 120, 60, "Player 1")
move2 = Button.Button(DISPLAYSURF, 820, 440, 120, 60, "Player 2")


# Functions
def playerRoll(player):
    # Get the current tile of the player
    tile = player.getCurrentTile()
    # Roll two dice
    dice = [random.randint(1, 6), random.randint(1, 6)]
    # Send a chat message to say what happened
    chat.send_chat('%s just rolled %i (%i, %i)' % (player.getUsername(), dice[0] + dice[1], dice[0], dice[1]))
    player.moveTo(tile + dice[0] + dice[1])

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            chat.destroy()
            pygame.quit()
            sys.exit(0)
        elif event.type == MOUSEBUTTONDOWN:
            if buy.pressed(pygame.mouse.get_pos()):
                # Buy func goes here
                print("buy")
            elif sell.pressed(pygame.mouse.get_pos()):
                # Sell function goes here
                print("sell")
            elif roll.pressed(pygame.mouse.get_pos()):
                # Roll function goes here
                print("Roll")
            elif endturn.pressed(pygame.mouse.get_pos()):
                # End turn func goes here
                print("End turn")
            elif move1.pressed(pygame.mouse.get_pos()):
                playerRoll(player1)
            elif move2.pressed(pygame.mouse.get_pos()):
                playerRoll(player2)
    pygame.display.update()
