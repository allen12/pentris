
class Pentomino:

	def __init__(self, shape, start_x, start_y = -1):
		# shape is the matrix of all possible templates of the shape
		# start_x and start_y are the coordinates relative to the BOARD!

		self.shape = shape
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