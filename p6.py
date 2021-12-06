import io

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		all_fish = input_stream.readline().strip().split(',')

		fish_hist = {key:0 for key in range(9)}
		for fish in all_fish:
			fish_hist[int(fish)] += 1

		return fish_hist


def simulate_life(fish_hist, num_days):

	simulated_fish = {key:fish_hist[key] for key in fish_hist}

	for _ in range(num_days):

		#do a day
		simulated_fish = {(key-1):simulated_fish[key] for key in simulated_fish}

		#give birth/reset cycle
		birthing = simulated_fish.pop(-1)
		simulated_fish[8] = birthing
		simulated_fish[6] += birthing

	return simulated_fish


fish_hist = load_stuff("input6.txt")
simulated_fish = simulate_life(fish_hist, 80)
print(sum(list(simulated_fish.values())))
simulated_fish = simulate_life(fish_hist, 256)
print(sum(list(simulated_fish.values())))
