import io

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		all_crab = input_stream.readline().strip().split(',')

		crab_hist = {}
		for crab in all_crab:
			crab = int(crab)
			if crab not in crab_hist:
				crab_hist[crab] = 0
			crab_hist[crab] += 1

		crab_hist = {key:crab_hist[key] for key in sorted(list(crab_hist.keys()))}

		return crab_hist


def split_crabs(crab_hist, part):
	
	crab_hist_keys = list(crab_hist.keys())

	"""
	brute force baby
	yes you don't have to check all pivots in part 1 
	only ones actually occupied by crabs but w/e
	"""
	best=float('inf')
	for pivot in range(crab_hist_keys[0],crab_hist_keys[-1] + 1):
		crab_pivot_sum = sum([calc_fuel(key,pivot,part)*crab_hist[key] for key in crab_hist])
		if crab_pivot_sum < best:
			best = crab_pivot_sum
		
	return(best)

	
def calc_fuel(start,end,part):

	dx = abs(end-start)
	if part == 1:
		return dx

	return dx*(dx+1)//2



crab_hist = load_stuff("input7.txt")

best_split = split_crabs(crab_hist, 1)
print(best_split)

best_split = split_crabs(crab_hist, 2)
print(best_split)


