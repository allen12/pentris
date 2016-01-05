""" Pentris, an extension of Tetris, with each piece having five instead of four
blocks (pentominos).

Allen Cheng | allen12@umd.edu | computer_allen@yahoo.com
"""

from copy import deepcopy
import random, time, pygame, sys
from pygame.locals import *

from board import Board
from factory import Factory
from pentomino import Pentomino


FPS = 60  # because every game should run at 60 fps!

WINDOW_WIDTH = 900      # can be adjusted 
WINDOW_HEIGHT = 675     # 4:3 aspect ratio preferred

MINO_SIZE = 26      # Length and width of a single mino block
BOARD_MINO_WIDTH = 12    # Number of minos te width of the playing field
BOARD_MINO_HEIGHT = 20   # Number of minos the height

BOARD_WIDTH = MINO_SIZE * BOARD_MINO_WIDTH     # Pixel width of board
BOARD_HEIGHT = MINO_SIZE * BOARD_MINO_HEIGHT   # Pixel height of board

LEFT_RIGHT_MARGIN = (WINDOW_WIDTH - BOARD_WIDTH)//2
TOP_MARGIN = WINDOW_HEIGHT - BOARD_HEIGHT - 10

MOVE_SIDEWAYS_TIME = 0.10      # delay to keep moving a pentomino sideways
SOFT_DROP_TIME = 0.08          # delay to keep soft dropping a pentomino

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

def main():
	global FPS_CLOCK, SPRITEBATCH
	pygame.init()
	FPS_CLOCK = pygame.time.Clock()
	SPRITEBATCH = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	pygame.display.set_caption("Pentris")

	background = pygame.Surface(SPRITEBATCH.get_size())
	background = background.convert()
	background.fill((0, 0, 0))
	font = pygame.font.Font(None, 255)
	text = font.render("Pentris", 1, (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)
	SPRITEBATCH.blit(background, (0, WINDOW_HEIGHT//2 - 100))
	pygame.display.flip()

	pygame.mixer.music.load('tetris.mid')   # start playing the tetris music
	pygame.mixer.music.play(-1, 0.0)        # loop indefinitely
	play()
	pygame.mixer.music.stop()
	quit()

def play():
	board = Board(BOARD_MINO_WIDTH, BOARD_MINO_HEIGHT, MINO_SIZE)
	factory = Factory()

	global lastFallTime, lastPlayerDownTime, lastPlayerSidewaysTime

	lastFallTime = time.time()             # last time the piece fell downwards by itself
	lastPlayerDownTime =  time.time()      # last time the player soft drops
	lastPlayerSidewaysTime = time.time()   # last time the player moves a piece sideways

	PENTOMINO_START_X = BOARD_MINO_WIDTH // 2 - 3   # coordinates of starting location

	currentPiece = Pentomino(factory.obtainShape(), getRandomColor(), PENTOMINO_START_X)
	nextPiece = Pentomino(factory.obtainShape(), getRandomColor(), PENTOMINO_START_X)

	goingDown = goingLeft = goingRight = False
	level = score = 0
	lines = 0
	fallTime = 0.5                         # how many seconds pass for piece to auto-fall one space

	while True: # infinite game loop

		if (currentPiece != None):
			print("currentPiece: " + str(currentPiece.x) + " " + str(currentPiece.y))

		checkQuit()

		# check if there is currently a pentomino in play. if not, generate a new one
		if currentPiece == None: 
			currentPiece = nextPiece
			nextPiece = Pentomino(factory.obtainShape(), getRandomColor(), PENTOMINO_START_X)

			# new piece can't fit on the board, game over!
			if not board.isPentominoValid(currentPiece):
				return

		handlePentominoMovement(board, currentPiece, goingDown, goingLeft, goingRight)

		# if current pieece has landed on the board, then clear any complete lines
		if handlePentominoFall(board, currentPiece, fallTime):
			board.addPentominoToBoard(currentPiece)
			currentPiece = None
			lines_cleared = board.checkForCompleteLines()
			lines += lines_cleared
			score += int(2250*lines_cleared**2 - 3850*lines_cleared + 900)
			level = lines // 10

		draw(board, currentPiece)
		FPS_CLOCK.tick(FPS)

def handlePentominoMovement(board, pentomino, goingDown, goingLeft, goingRight):
	global lastPlayerDownTime, lastPlayerSidewaysTime

	if time.time() - lastPlayerSidewaysTime > MOVE_SIDEWAYS_TIME:
		if goingLeft:
			pentomino.moveLeft()
			if not board.isPentominoValid(pentomino):
				pentomino.moveRight()
			else:
				lastPlayerSidewaysTime = time.time()
		if goingRight:
			pentomino.moveRight()
			if not board.isPentominoValid(pentomino):
				pentomino.moveLeft()
			else:
				lastPlayerSidewaysTime = time.time()

	if time.time() - lastPlayerDownTime > SOFT_DROP_TIME:
		if goingDown:
			pentomino.moveDown()
			if not board.isPentominoValid(pentomino):
				pentomino.moveUp()
			else:
				lastPlayerDownTime = time.time()


def handlePentominoFall(board, pentomino, fallTime):
	# Handles the natural fall of the pentomino without user action.
	# Returns True if the pentomino has landed as far as possible and is ready
	# to be permanently added to the board
	global lastFallTime

	if time.time() - lastFallTime > fallTime:
		pentomino_copy = deepcopy(pentomino)
		pentomino_copy.moveDown()

		if board.isPentominoValid(pentomino_copy):
			pentomino.moveDown()
			lastFallTime = time.time()
			return False
		else:
			return True

def draw(board, pentomino):
	SPRITEBATCH.fill(BLACK)
	board.drawBoard(SPRITEBATCH, LEFT_RIGHT_MARGIN, TOP_MARGIN)

	if pentomino != None:
		board.drawPentomino(SPRITEBATCH, pentomino, LEFT_RIGHT_MARGIN, TOP_MARGIN)

	pygame.display.update()

def checkQuit():
	if pygame.event.peek(QUIT):
		quit()

	for event in pygame.event.get(KEYUP):
		if event.key == K_ESCAPE:
			quit()
		else:
			pygame.event.post(event)

def quit():
	pygame.quit()
	sys.exit()


def getRandomColor():
	return random.choice(COLORS)


if __name__ == '__main__':
	main()