import io
import copy

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		dots = set()			
		input_line = input_stream.readline().strip()
		while len(input_line) > 0:
			x,y = [int(d) for d in input_line.split(',')]
			dots.add((x,y))
			input_line = input_stream.readline().strip()

		fold_instructions = []
		for input_line in input_stream:
			_,_,instruction = input_line.strip().split(' ')
			direction,position = instruction.split('=')
			position = int(position)
			fold_instructions.append((direction, position))

		return dots, fold_instructions


#obvs don't request more folds than exist (unless part2 asks us to loop?)
def simulate_fold_paper(dots, fold_instructions, number_of_folds):

	if isinstance(number_of_folds, str):
		number_of_folds = len(fold_instructions)

	#incase part 2 wants all folds
	dots = copy.deepcopy(dots)	

	for fold_i in range(number_of_folds):

		fold_instruction = fold_instructions[fold_i]
		dots = do_fold(dots, fold_instruction)

	return dots


def do_fold(dots, fold_instruction):

	direction, position = fold_instruction

	#if direction is y transpose
	if direction == 'y':
		dots = [(y,x) for x,y in dots]

	folded_dots = set()
	for dot in dots:

		x,y = dot
		
		#problem says dots will never be on fold
		#if the dot is below the fold, fold it
		if position < x:
			x = 2*position - x
		
		folded_dots.add((x,y))

	#can a fold create a new (0,0) position? 
	#not relevant for part 1, but may change things for part 2 (will have to shift things)
	#guess not

	#if direction is y untranspose
	if direction == 'y':
		folded_dots = [(y,x) for x,y in folded_dots]

	return folded_dots


def display_dots(dots):	

	#it's sideways
	dots = [(y,x) for x,y in dots]

	h = max([x for x,y in dots]) + 1
	w = max([y for x,y in dots]) + 1

	display = [['.' for y in range(w)] for x in range(h)]

	for x,y in dots:
		display[x][y] = '#'
	
	output = ""
	for display_line in display:
		for d in display_line:
			output += d
		output+='\n'
	
	print(output)


dots, fold_instructions = load_stuff("input13.txt")
folded_dots = simulate_fold_paper(dots, fold_instructions, 1)
print(len(folded_dots))
folded_dots = simulate_fold_paper(dots, fold_instructions, 'all')
display_dots(folded_dots)
