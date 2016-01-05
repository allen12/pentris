""" Generic pentomino class representing a shape with five minos. The input
shape should come from factory.py and is a list of all of the possible
rotations of the particular shape.

Only ONE pentomino should be active in play on the board at any one time. Once
the pentomino has been settled on the board, it should be added to the board permanently.
"""
class Pentomino:

	def __init__(self, shape, color, start_x, start_y = -1):
		# shape is the matrix of all possible templates of the shape
		# start_x and start_y are the coordinates relative to the BOARD!
		# by default, start_y starts above the actual board
		self.shape = shape
		self.color = color
		self.rotation = 0
		self.x = start_x
		self.y = start_y

	def getCurrentTemplate(self):
		return self.shape[self.rotation]

	def rotateClockwise(self):
		# changes the rotation state and returns the corresponding template
		self.rotation = (self.rotation + 1) % len(self.shape)
		return self.shape[self.rotation]

	def rotateCounterclockwise(self):
		# changes the rotation state and returns the corresponding template
		self.rotation = (self.rotation - 1) % len(self.shape)
		return self.shape[self.rotation]

	def moveLeft(self):
		self.x -= 1

	def moveRight(self):
		self.x += 1

	def moveDown(self):
		self.y += 1

	def moveUp(self):
		self.y -= 1