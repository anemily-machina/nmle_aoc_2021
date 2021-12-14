import io
import copy

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		#get template (extra space is for last character bookkeeping)
		#I assume they fix it so the last character is either the most or least
		#so this bookkeepping is required?
		template = input_stream.readline().strip() + ' '

		poly_hist = {}
		for p_i in range(len(template) - 1):
			twoelem = template[p_i:p_i+2]			
			if twoelem not in poly_hist:
				poly_hist[twoelem] = 0				
			poly_hist[twoelem] += 1

		#remove new line
		input_stream.readline()

		rules = {}
		for input_line in input_stream:
			pair, insertion = input_line.strip().split(' -> ')
			rules[pair] = insertion

		return poly_hist, rules


def simulate_insertions(poly_hist, rules, num_insertions):

	poly_hist = copy.deepcopy(poly_hist)

	for _ in range(num_insertions):

		poly_hist = do_insertions(poly_hist, rules)

	return poly_hist


def do_insertions(poly_hist, rules):
	
	new_poly_hist = {}

	for twoelem in poly_hist:

		if twoelem in rules:
			new_elem = rules[twoelem]
			new_twoelems = [twoelem[0] + new_elem, new_elem + twoelem[1]]
		else:
			new_twoelems = [twoelem]

		for new_twoelem in new_twoelems:
			if new_twoelem not in new_poly_hist:
				new_poly_hist[new_twoelem] = 0
			new_poly_hist[new_twoelem] += poly_hist[twoelem]

	return new_poly_hist


def calc_most_minus_least(poly_hist):

	elem_hist = {}

	#add all values based on left element
	#bookeeping in loading makes this count the last element
	for twoelem in poly_hist:
		elem = twoelem[0]
		if elem not in elem_hist:
			elem_hist[elem] = 0
		elem_hist[elem] += poly_hist[twoelem]

	max_e = max(list(elem_hist.values()))
	min_e = min(list(elem_hist.values()))

	return max_e - min_e


poly_hist, rules= load_stuff("input14.txt")
simualted_poly_hist = simulate_insertions(poly_hist, rules, 10)
most_minus_least = calc_most_minus_least(simualted_poly_hist)
print(most_minus_least)
simualted_poly_hist = simulate_insertions(poly_hist, rules, 40)
most_minus_least = calc_most_minus_least(simualted_poly_hist)
print(most_minus_least)
