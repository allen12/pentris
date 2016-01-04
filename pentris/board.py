"""

Board class representing the playing field. The board matrix holds data
about colors and is represented by a grid of arbitrary size, constructed
at runtime.

"""

import factory, pygame
from pygame.locals import *

class Board:

	EMPTY = "."

	# COLOR DEFINITIONS
	#          ( R ,  G ,  B )
	BLUE     = (  0,   0, 255)
	FUSCHIA  = (255,   0, 255)
	GREEN    = (  0, 128,   0)
	AQUA     = (  0, 255, 255)
	BLACK    = (  0,   0,   0)
	LIME     = (  0, 255,   0)
	NAVY_BLU = (  0,   0, 128)
	PURPLE   = (128,   0, 128)
	RED      = (255,   0,   0)
	SILVER   = (192, 192, 192)
	TEAL     = (  0, 128, 128)
	WHITE    = (255, 255, 255)
	YELLOW   = (255, 255,   0)

	COLORS = (AQUA, BLUE, FUSCHIA, GREEN, LIME, NAVY_BLU, PURPLE,
				RED, SILVER, TEAL, WHITE, YELLOW)


	def __init__(self, board_width, board_height, mino_size):
		# Create an empty board and store instance variables
		self.board = []

		for i in range(self.board_height):
			self.board.append([EMPTY] * board_width)

		self.MINO_SIZE = mino_size
		self.BOARD_WIDTH = board_width
		self.BOARD_HEIGHT = board_height

	def isLineComplete(self, y):
		#  Given a specific row on the board, return whether the row is filled with minos.
		if y < 0 or y >= self.BOARD_WIDTH:
			raise ValueError("passed-in y does not exist on the board!")

		for x in range(self.BOARD_WIDTH):
			if self.board[y][x] == EMPTY:
				return False

		return True

	def checkForCompleteLines(self):
		# Removes any completed lines from the board and returns the number removed.
		numLines = 0

		# check each row, start from bottom of board
		for y in range(self.BOARD_HEIGHT - 1, -1, -1):
			if self.isLineComplete(y):
				# shift every row above down one row
				for row in range(y-1, -1, -1):
					self.board[row+1] = self.board[row]

				# remove the top line
				self.board[0] = [EMPTY]*self.BOARD_WIDTH

				# On the next iteration, make sure we check te line we just pulled down
				y += 1
				numLines += 1

		return numLines

	def drawBoard(self, spritebatch, x_coord, y_coord):
		# draws the board and its contents
		# x_coord and y_coord, where to draw the board, are to be handled by client functions

		# draws border around the board
		pygame.draw.rect(spritebatch, self.SILVER, (x_coord, y_coord-7, 
			(self.BOARD_WIDTH*self.MINO_SIZE)+8, (self.BOARD_HEIGHT*self.MINO_SIZE)+8), 5)

		# fills the background of the board
		pygame.draw.rect(spritebatch, self.BLACK, 
			(x_coord, y_coord, self.MINO_SIZE*self.BOARD_WIDTH, self.MINO_SIZE*self.BOARD_HEIGHT))

		# draws each individual mino on the board
		for y in range(self.BOARD_HEIGHT):
			for x in range(self.BOARD_WIDTH):
				if board[y][x] != ".":
					self.drawMino(spritebatch, x, y, board[y][x], x_coord, y_coord)

	def drawMino(self, spritebatch, mino_x, mino_y, color, board_x, board_y):
		# color should be an RGB tuple
		# mino_x and mino_y are the INDICIES of the minos on the board, NOT their pixel locations
		# board_x and board_y ARE the pixel locations of the top-left corner of the board
		pixel_x = board_x + (mino_x * self.MINO_SIZE)
		pixel_y = board_y + (mino_y * self.MINO_SIZE)

		pygame.draw.rect(spritebatch, color, (pixel_x+1, pixel_y+1, self.MINO_SIZE-1, self.MINO_SIZE-1))

	def drawPentomino(self, spritebatch, pentomino, board_x, board_y):
		template = pentomino.getCurrentTemplate()

		for y in range(len(template)):
			for x in range(len(template[0])):
				if (template[y][x] != self.EMPTY):
					self.drawMino(spritebatch, pentomino.x, pentomino.y, pentomino.color, board_x, board_y)

	def isOnTheBoard(self, x, y):
    	return x >= 0 and x < self.BOARD_WIDTH and y < self.BOARD_HEIGHT

	def isPentominoValid(self, pentomino):
		template = pentomino.getCurrentTemplate()

		for y in range(len(template)):
			for x in range(len(template[0])):
				if (template[y][x] == self.EMPTY):
					continue

				mino_x = pentomino.x + x
				mino_y = pentomino.y + y

				if not isOnTheBoard(mino_x, mino_y):
					return False
				if self.board[mino_y][mino_x] != self.EMPTY:
					return False

		return True