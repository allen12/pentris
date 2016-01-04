"""

Board class representing the playing field. The board matrix holds data
about colors and is represented by a grid of arbitrary size, constructed
at runtime.

"""

import factory, pygame
from pygame.locals import *

class Board:

	EMPTY = "."

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