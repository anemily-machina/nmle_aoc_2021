import io
import numpy as np

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 
		bingo_balls = [int(b) for b in input_stream.readline().strip().split(',')]	

		#load all the boards at once so I don't have to deal with newlines
		boards = []
		for line in input_stream:		
			boards += [int(n) for n in line.strip().split()]

		#seperate the boards
		boards = np.array_split(boards, len(boards)//25)
		marks = np.zeros((len(boards), len(boards[0])), dtype=np.int8)	

	return bingo_balls, boards, marks


def get_matches(ball, boards):

	board_i = []
	number_i = []
	for b_i, board in enumerate(boards):
		n_i = np.where(board==ball)
		n_i = n_i[0]		
		if len(n_i) > 0:
			board_i.append(b_i)
			number_i.append(n_i[0]) #it can only appear once

	return board_i, number_i


def mark_matches(marks, board_i, number_i):

	for b_i, n_i in zip(board_i, number_i):
		marks[b_i][n_i] = 1


def check_bingo(marks, board_i, number_i):

	#check for bingo
	#only check specific board,row,col that changed
	bingo_i = []
	for b_i, n_i in zip(board_i, number_i):

		mark = marks[b_i]	

		row = n_i // 5
		row_bingo = True
		for j in range(5):	
			row_bingo = row_bingo and (mark[row*5 + j] == 1)

		col = n_i % 5
		col_bingo = True
		for j in range(5):	
			col_bingo = col_bingo and (mark[j*5 + col] == 1)

		bingo = row_bingo or col_bingo
		
		if bingo:
			bingo_i.append(b_i)

	return bingo_i


def get_score(boards, marks, bingo_i, ball):

	scores = []

	for b_i in bingo_i:

		board = boards[b_i]
		mark = marks[b_i]

		unmarked_sum = sum([b if m == 0 else 0 for b,m in zip(board, mark)])

		scores.append(unmarked_sum*ball)

	#this is technically wrong if there is a tie for last we will get the wrong number
	#however the specification of the question implies there will not be ties for first or last?
	return max(scores)


def play_bingo(bingo_balls, boards, marks):

	scores = []

	for ball in bingo_balls:

		board_i, number_i = get_matches(ball, boards)
		mark_matches(marks, board_i, number_i)

		bingo_i = check_bingo(marks, board_i, number_i)

		if len(bingo_i) > 0:
			#get the first score and last score
			if (len(scores) == 0) or (len(boards) == 1):
				scores.append(get_score(boards, marks, bingo_i, ball))

				if (len(boards) == 1):
					return scores

			boards = np.delete(boards, bingo_i, axis=0)			
			marks = np.delete(marks, bingo_i, axis=0)		



bingo_balls, boards, marks = load_stuff("input4.txt")
scores = play_bingo(bingo_balls, boards, marks)
print(scores)
