import io
from collections import deque

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		all_lines = []

		#yes we could check for local minimums here but I will load it all this time		
		for input_line in input_stream:
			all_lines.append(input_line.strip())
		
		return all_lines 


def process_line(line):

	matches = {'(':')','[':']','{':'}','<':'>'}

	stack = deque()

	#check each character
	for b in line:
		
		#if it is an open bracket push the match
		if b in matches:
			stack.append(matches[b])
		#oterhwise it is a closed bracket, make sure it is the correct one
		else:
			close = stack.pop()
			if b != close:
				return b

	#if we are here the stack (possibly empty) is what is needed to complete the line
	return stack


def process_lines(all_lines):
	
	errors = []
	completions = []
	for line in all_lines:

		processed_line = process_line(line)

		#all lines are errored in some way so this logic is fine
		if isinstance(processed_line, deque):			
			completions.append(processed_line)
		else:
			errors.append(processed_line)

	return errors, completions


def score_errors(errors):
	
	b_scores = {')':3,']':57,'}':1197,'>':25137}
	total_score = sum([b_scores[e] for e in errors])
	return total_score


def score_completions(completions):

	b_scores = {')':1,']':2,'}':3,'>':4}
	scores = []

	for completion in completions:

		score = 0
		while len(completion) > 0:
			b = completion.pop()
			score = score*5 + b_scores[b]

		scores.append(score)

	scores = sorted(scores)
	middle_score = scores[len(scores)//2]

	return middle_score


all_lines = load_stuff("input10.txt")
errors, completions = process_lines(all_lines)
errors_score = score_errors(errors)
print(errors_score)
completions_score = score_completions(completions)
print(completions_score)


