""" Pentris, an extension of Tetris, with each piece having five instead of four
blocks (pentominos).

Allen Cheng | allen12@umd.edu | computer_allen@yahoo.com
https://github.com/allen12/pentris
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
BOARD_MINO_WIDTH = 14    # Number of minos te width of the playing field
BOARD_MINO_HEIGHT = 24   # Number of minos the height

BOARD_WIDTH = MINO_SIZE * BOARD_MINO_WIDTH     # Pixel width of board
BOARD_HEIGHT = MINO_SIZE * BOARD_MINO_HEIGHT   # Pixel height of board

LEFT_RIGHT_MARGIN = (WINDOW_WIDTH - BOARD_WIDTH)//2
TOP_MARGIN = WINDOW_HEIGHT - BOARD_HEIGHT - 10

MOVE_SIDEWAYS_TIME = 0.12      # delay to keep moving a pentomino sideways
SOFT_DROP_TIME = 0.06          # delay to keep soft dropping a pentomino

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

TEXTCOLOR = WHITE

def main():
	global FPS_CLOCK, SPRITEBATCH, BASICFONT

	pygame.init()
	FPS_CLOCK = pygame.time.Clock()
	BASICFONT = pygame.font.Font(None, 36)
	SPRITEBATCH = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

	# start playing the background music
	pygame.mixer.music.load('tetris_m_cut.mp3')   # start playing the tetris music
	pygame.mixer.music.set_volume(0.5)
	pygame.mixer.music.play(-1, 0.0)        # loop indefinitely

	play()

	pygame.mixer.music.stop()

	quit()

def play():

	global lastFallTime, lastPlayerDownTime, lastPlayerSidewaysTime, score

	board = Board(BOARD_MINO_WIDTH, BOARD_MINO_HEIGHT, MINO_SIZE)
	factory = Factory()

	lastFallTime = time.time()             # last time the piece fell downwards by itself
	lastPlayerDownTime =  time.time()      # last time the player soft drops
	lastPlayerSidewaysTime = time.time()   # last time the player moves a piece sideways

	PENTOMINO_START_X = BOARD_MINO_WIDTH // 2 - 3   # coordinates of starting location
	PENTOMINO_START_Y = -1

	# initialize the starting pentomino pieces
	currentPiece = Pentomino(factory.obtainShape(), getRandomColor(), PENTOMINO_START_X)
	nextPiece = Pentomino(factory.obtainShape(), getRandomColor(), PENTOMINO_START_X)
	holdPiece = None

	usedHold = False    # Set to true if player uses "Hold" on the current piece

	# keep track of whether piece is currently moving or not through the game loop
	goingDown = goingLeft = goingRight = False

	level = 0
	score = 0
	lines = 0

	fallTime = 1.00 - level*0.08         # how many seconds pass for piece to auto-fall one space

	while True: # infinite game loop

		# if (currentPiece != None):
		# 	print("currentPiece: " + str(currentPiece.x) + " " + str(currentPiece.y))

		checkQuit()

		# check if there is currently a pentomino in play. if not, generate a new one
		if currentPiece == None: 
			currentPiece = nextPiece
			nextPiece = Pentomino(factory.obtainShape(), getRandomColor(), PENTOMINO_START_X)

			# new piece can't fit on the board, game over!
			if not board.isPentominoValid(currentPiece):
				return

		# if piece is currently detected as moving sideways or soft dropping, do that
		handlePentominoMovement(board, currentPiece, goingDown, goingLeft, goingRight)

		# handle user input events
		for event in pygame.event.get(KEYUP):
			if event.key == K_LEFT:
				goingLeft = False
			elif event.key == K_RIGHT:
				goingRight = False
			elif event.key == K_DOWN:
				goingDown = False

		for event in pygame.event.get(KEYDOWN):
			# sideways movements
			if event.key == K_LEFT:
				currentPiece.moveLeft()
				if not board.isPentominoValid(currentPiece):
					currentPiece.moveRight()
				else:
					goingLeft = True
					lastPlayerSidewaysTime = time.time()
			elif event.key == K_RIGHT:
				currentPiece.moveRight()
				if not board.isPentominoValid(currentPiece):
					currentPiece.moveLeft()
				else:
					lastPlayerSidewaysTime = time.time()
					goingRight = True

			# soft drop movements
			elif event.key == K_DOWN:
				currentPiece.moveDown()
				if not board.isPentominoValid(currentPiece):
					currentPiece.moveUp()
				else:
					lastPlayerDownTime = time.time()
					goingDown = True
					score += 1

			# hard drop movements
			elif event.key == K_SPACE:

				hold = pygame.mixer.Sound("harddrop.ogg") 
				hold.play()

				while board.isPentominoValid(currentPiece):
					currentPiece.moveDown()
					score += 2

				score -= 2
				currentPiece.moveUp()

			# rotations
			elif event.key == K_UP:
				currentPiece.rotateClockwise()
				if not board.isPentominoValid(currentPiece):
					currentPiece.rotateCounterclockwise()

			elif event.key == K_z:
				currentPiece.rotateCounterclockwise()
				if not board.isPentominoValid(currentPiece):
					currentPiece.rotateClockwise()

			# hold
			elif event.key == K_LSHIFT or event.key == K_RSHIFT:
				if usedHold:    # not allowed to hold more than once per falling piece
					continue

				hold = pygame.mixer.Sound("hold.wav")   # play "hold" sound effect
				hold.play()

				usedHold = True
				# reset piece orientation
				currentPiece.x = PENTOMINO_START_X
				currentPiece.y = PENTOMINO_START_Y
				currentPiece.rotation = 0

				tempPiece = holdPiece    # swap hold and currentPiece
				holdPiece = currentPiece
				currentPiece = tempPiece

				if currentPiece == None:
					currentPiece = nextPiece
					nextPiece = Pentomino(factory.obtainShape(), getRandomColor(), PENTOMINO_START_X)

				# reset piece orientation
				currentPiece.x = PENTOMINO_START_X
				currentPiece.y = PENTOMINO_START_Y
				currentPiece.rotation = 0

		# if current piece has landed on the board, then clear any complete lines
		if handlePentominoFall(board, currentPiece, fallTime):
			global MOVE_SIDEWAYS_TIME, SOFT_DROP_TIME

			board.addPentominoToBoard(currentPiece)     # permanently add to board
			usedHold = False
			currentPiece = None

			lines_cleared = board.checkForCompleteLines()    # obtain how many lines cleared
			lines += lines_cleared

			if lines_cleared == 1:                 # adjust score as necessary
				score += 1000 * (level+1)
			elif lines_cleared == 2:
				score += 3500 * (level+1)
			elif lines_cleared == 3:
				score += 7000 * (level+1)
			elif lines_cleared == 4:
				score += 15000 * (level+1)
			elif lines_cleared == 5:
				score += 35000 * (level+1)

			# calculate increases in level and difficulty, if necessary
			level = lines // 5
			fallTime = 1.00 - level * 0.08
			MOVE_SIDEWAYS_TIME = 0.12 - level * 0.01
			SOFT_DROP_TIME = 0.06 - level * 0.01
			if fallTime < 0.03:
				fallTime = 0.03

		# draw everything, including the board and status updates
		draw(board, currentPiece, nextPiece, holdPiece, level, score, lines)
		pygame.event.pump()   # needed if no user input events in a while, otherwise game freezes
		FPS_CLOCK.tick(FPS)

def handlePentominoMovement(board, pentomino, goingDown, goingLeft, goingRight):
	global lastPlayerDownTime, lastPlayerSidewaysTime, score

	# only allow moving sideways if it has been MOVE_SIDEWAYS_TIME seconds since last movement
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

	# similar action with soft dropping / moving downwards
	if time.time() - lastPlayerDownTime > SOFT_DROP_TIME:
		if goingDown:
			pentomino.moveDown()
			if not board.isPentominoValid(pentomino):
				pentomino.moveUp()
			else:
				lastPlayerDownTime = time.time()
				score += 1


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

def draw(board, pentomino, next_pentomino, hold_petrimino, level, score, lines):
	global SPRITEBATCH, BASICFONT

	SPRITEBATCH.fill(BLACK)
	board.drawBoard(SPRITEBATCH, LEFT_RIGHT_MARGIN, TOP_MARGIN)

    # draw the score text
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
	scoreRect = scoreSurf.get_rect()
	scoreRect.topleft = (WINDOW_WIDTH - 250, 30)
	SPRITEBATCH.blit(scoreSurf, scoreRect)

    # draw the level text
	levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.topleft = (WINDOW_WIDTH - 250, 70)
	SPRITEBATCH.blit(levelSurf, levelRect)

    # draw the lines text
	levelSurf = BASICFONT.render('Lines: %s' % lines, True, TEXTCOLOR)
	levelRect = levelSurf.get_rect()
	levelRect.topleft = (WINDOW_WIDTH - 250, 110)
	SPRITEBATCH.blit(levelSurf, levelRect)

	# draw the "next" piece
	nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
	nextRect = nextSurf.get_rect()
	nextRect.topleft = (120, WINDOW_HEIGHT - 120)
	SPRITEBATCH.blit(nextSurf, nextRect)
	board.drawPentominoPixels(SPRITEBATCH, next_pentomino, 120 - MINO_SIZE, WINDOW_HEIGHT - 80)

	# draw the "hold" piece
	holdSurf = BASICFONT.render('Hold:', True, TEXTCOLOR)
	holdRect = holdSurf.get_rect()
	holdRect.topleft = (120, 60)
	SPRITEBATCH.blit(holdSurf, holdRect)

	if hold_petrimino != None:
		board.drawPentominoPixels(SPRITEBATCH, hold_petrimino, 120 - MINO_SIZE, 100)
	
	if pentomino != None:
		board.drawGhostPentomino(SPRITEBATCH, pentomino, LEFT_RIGHT_MARGIN, TOP_MARGIN)
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