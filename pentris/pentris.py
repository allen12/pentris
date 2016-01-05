""" Pentris, an extension of Tetris, with each piece having five instead of four
blocks (pentominos).

Allen Cheng | allen12@umd.edu | computer_allen@yahoo.com
"""

import random, time, pygame, sys
from pygame.locals import *
from board import Board
from factory import Factory
from pentomino import Pentomino

FPS = 60  # because every game should run at 60 fps!

WINDOW_WIDTH = 900      # can be adjusted 
WINDOW_HEIGHT = 675     # 4:3 aspect ratio preferred

MINO_SIZE = 26      # Length and width of a single mino block
BOARD_MINO_WIDTH = 10    # Number of minos te width of the playing field
BOARD_MINO_HEIGHT = 20   # Number of minos the height

BOARD_WIDTH = MINO_SIZE * BOARD_MINO_WIDTH     # Pixel width of board
BOARD_HEIGHT = MINO_SIZE * BOARD_MINO_HEIGHT   # Pixel height of board

LEFT_RIGHT_MARGIN = (WINDOW_WIDTH - BOARD_WIDTH)//2
TOP_MARGIN = WINDOW_HEIGHT - BOARD_HEIGHT - 10

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
	
	screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))
	font = pygame.font.Font(None, 255)
	text = font.render("Pentris", 1, (255, 255, 255))
	textpos = text.get_rect()
	textpos.centerx = background.get_rect().centerx
	background.blit(text, textpos)
	screen.blit(background, (0, WINDOW_HEIGHT//2 - 100))
	pygame.display.flip()

	pygame.mixer.music.load('tetris.mid')   # start playing the tetris music
	pygame.mixer.music.play(-1, 0.0)        # loop indefinitely
	play()

	while True:
		pass

	pygame.mixer.music.stop()
	quit()

def play():
	board = Board(BOARD_WIDTH, BOARD_HEIGHT, MINO_SIZE)
	

def quit():
	pygame.quit()
	sys.exit()

if __name__ == '__main__':
	main()
