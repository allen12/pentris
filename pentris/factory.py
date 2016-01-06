"""
Helper class to manage random generation of pentominos. The naming scheme of
pentomino shapes is used as follows: F, F', I, L, J, N, N', P, Q, T, U, V, 
W, X, Y, Y', Z, S.

With the 18 possible shapes, this class ensures that each set of 18 generated
shapes will have one of each possible shape.
"""

from random import shuffle, randrange

class Factory:

	F_SHAPE = [["..OO.",
				".OO..",
				"..O.."],
			   ["..O..",
			    ".OOO.",
			    "...O."],
			   ["..O..",
			   	"..OO.",
			   	".OO.."],
			   [".O...",
			    ".OOO.",
			    "..O.."]]

	F_PRIME_SHAPE = [[".OO..",
					  "..OO.",
					  "..O.."],
					 ["...O.",
					  ".OOO.",
					  "..O.."],
					 ["..O..",
					  ".OO..",
					  "..OO."],
					 ["..O..",
					  ".OOO.",
					  ".O..."]]

	I_SHAPE = [[".OOOOO."],
			   [".O.",
			    ".O.",
			    ".O.",
			    ".O.",
			    ".O."]]

	L_SHAPE = [["....O.",
				".OOOO."],
			   [".O..",
			    ".O..",
			    ".O..",
			    ".OO."],
			   [".OOOO.",
			    ".O...."],
			   [".OO.",
			    "..O.",
			    "..O.",
			    "..O."]]

	J_SHAPE = [[".O....",
				".OOOO."],
			   [".OO.",
			    ".O..",
			    ".O..",
			    ".O.."],
			   [".OOOO.",
			    "....O."],
			   ["..O.",
			    "..O.",
			    "..O.",
			    ".OO."]]

	N_SHAPE = [[".OOO..",
	            "...OO."],
	           ["..O.",
	            "..O.",
	            ".OO.",
	            ".O.."],
	           [".OO...",
	            "..OOO."],
	           ["..O.",
	            ".OO.",
	            ".O..",
	            ".O.."]]

	N_PRIME_SHAPE = [["..OOO.",
					  ".OO..."],
					 [".O..",
					  ".OO.",
					  "..O.",
					  "..O."],
					 ["...OO.",
					  ".OOO.."],
					 [".O..",
					  ".O..",
					  ".OO.",
					  "..O."]]

	P_SHAPE = [[".OO.",
				".OO.",
				".O.."],
			   [".OOO.",
			    "..OO."],
			   ["..O.",
			    ".OO.",
			    ".OO."],
			   [".OO..",
			    ".OOO."]]

	Q_SHAPE = [[".OO.",
				".OO.",
				"..O."],
			   ["..OO.",
			    ".OOO."],
			   [".O..",
			    ".OO.",
			    ".OO."],
			   [".OOO.",
			    ".OO.."]]

	T_SHAPE = [["..O..",
			    "..O..",
			    ".OOO."],
			   [".O...",
			    ".OOO.",
			    ".O..."],
			   [".OOO.",
			    "..O..",
			    "..O.."],
			   ["...O.",
			    ".OOO.",
			    "...O."]]

	U_SHAPE = [[".O.O.",
				".OOO."],
			   [".OO.",
			    ".O..",
			    ".OO."],
			   [".OOO.",
			    ".O.O."],
			   [".OO.",
			    "..O.",
			    ".OO."]]

	V_SHAPE = [[".O...",
				".O...",
				".OOO."],
			   [".OOO.",
			    ".O...",
			    ".O..."],
			   [".OOO.",
			    "...O.",
			    "...O."],
			   ["...O.",
			    "...O.",
			    ".OOO."]]

	W_SHAPE = [[".O...",
				".OO..",
				"..OO."],
			   ["..OO.",
			    ".OO..",
			    ".O..."],
			   [".OO..",
			    "..OO.",
			    "...O."],
			   ["...O.",
			    "..OO.",
			    ".OO.."]]

	X_SHAPE = [["..O..",
				".OOO.",
				"..O.."]]

	Y_SHAPE = [["...O..",
			    ".OOOO."],
			   [".O..",
			    ".O..",
			    ".OO.",
			    ".O.."],
			   [".OOOO.",
			    "..O..."],
			   ["..O.",
				".OO.",
				"..O.",
				"..O."]]

	Y_PRIME_SHAPE = [["..O...",
					  ".OOOO."],
					 [".O..",
					  ".OO.",
					  ".O..",
					  ".O.."],
					 [".OOOO.",
					  "...O.."],
					 ["..O.",
					  "..O.",
					  ".OO.",
					  "..O."]]

	Z_SHAPE = [[".OO..",
				"..O..",
				"..OO."],
			   ["...O.",
			    ".OOO.",
			    ".O..."]]

	S_SHAPE = [["..OO.",
				"..O..",
				".OO.."],
			   [".O...",
			    ".OOO.",
			    "...O."]]

	SHAPES = [F_SHAPE, F_PRIME_SHAPE, I_SHAPE, L_SHAPE, J_SHAPE,
		  N_SHAPE, N_PRIME_SHAPE, P_SHAPE, Q_SHAPE, T_SHAPE,
		  U_SHAPE, V_SHAPE, W_SHAPE, X_SHAPE, Y_SHAPE,
		  Y_PRIME_SHAPE, Z_SHAPE, S_SHAPE]


	def __init__(self):
		self.queue = list(self.SHAPES)
		shuffle(self.queue)

	def obtainShape(self):
		random_index = randrange(0, len(self.queue))
		ret = self.queue.pop(random_index)

		if not self.queue:  # queue is empty!
			self.queue = list(self.SHAPES)
			shuffle(self.queue)

		return ret