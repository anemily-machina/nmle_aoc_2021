from collections import deque
import copy
import io

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		all_octo = []

		#yes we could check for local minimums here but I will load it all this time		
		for input_line in input_stream:
			all_octo.append([int(o) for o in input_line.strip()])
		
		return all_octo 


def simulate_steps(all_octo, num_steps, simulate_till_flash=False):

	simualted_octo = copy.deepcopy(all_octo)

	total_octo = len(simualted_octo)*len(simualted_octo[0])
	all_flash_step = -1

	octo_flashes = 0
	step_n = 0
	while (step_n < num_steps) or (simulate_till_flash and (all_flash_step == -1)):

		simualted_octo, flashed_octo = simulate_step(simualted_octo)

		#only update the count if we still need to
		if (step_n < num_steps):
			octo_flashes += len(flashed_octo)		

		step_n += 1

		#do this here as step #s start from 0
		if (all_flash_step == -1) and (len(flashed_octo) == total_octo):
			all_flash_step = step_n

	return octo_flashes, all_flash_step


def simulate_step(simualted_octo):

	#all octo increse by 1
	simualted_octo = [[o+1 for o in simualted_octo_row] for simualted_octo_row in simualted_octo]

	flashed_octo = set()
	to_flash = deque()

	#add all octo that will flash
	for i in range(len(simualted_octo)):
		for j in range(len(simualted_octo[0])):
			if simualted_octo[i][j] == 10:
				to_flash.append((i,j))

	#do flashes until we have no more flashes to do
	while len(to_flash) > 0:
		
		#get the next octo that might flash
		flashing_o = to_flash.popleft()

		#simulate the flash
		simualted_octo, new_to_flash = simulate_flash(simualted_octo, flashing_o)

		#add new octo's that will flash
		to_flash += new_to_flash

		flashed_octo.add(flashing_o)

	#set all flashed ocot's to 0
	for o_i, o_j in flashed_octo:
		simualted_octo[o_i][o_j] = 0


	return simualted_octo, flashed_octo


def simulate_flash(simualted_octo, flashing_o):

	h = len(simualted_octo)
	w = len(simualted_octo[0])

	#get the adjacent octo to the flasher
	o_i, o_j  = flashing_o
	adjacent_o = get_adjacent(o_i, o_j, h, w, diag=True)
	new_to_flash = []
	
	#increase the adjacent octo and if they are 10 note they will flash
	#(if it is greater than 10 it has already flashed or is in the queue to flash)
	for a_o in adjacent_o:
		
		a_o_i, a_o_j = a_o		

		simualted_octo[a_o_i][a_o_j] += 1

		if simualted_octo[a_o_i][a_o_j] == 10:
			new_to_flash.append(a_o)

	return simualted_octo, new_to_flash


def get_adjacent(i,j,h,w,diag=False):	

	#calculate offsets
	coords = []
	for offset in [-1,1]:
		coords.append((i, j+offset))
		coords.append((i+offset, j))
	if diag:
		for offset_i in [-1,1]:
			for offset_j in [-1,1]:	
				coords.append((i+offset_i, j+offset_j))

	#filter to only inbounds coords
	good_coords = []
	for coord in coords:
		
		c_i, c_j = coord
		if (c_i > -1) and (c_i < h) and (c_j > -1) and (c_j < w):
			good_coords.append(coord)

	return good_coords


all_octo = load_stuff("input11.txt")
flashed_octo, all_flash_step = simulate_steps(all_octo, 100, simulate_till_flash=True)
print(flashed_octo)
print(all_flash_step)


