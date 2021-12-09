import io
from collections import deque

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		height_map = []

		#yes we could check for local minimums here but I will load it all this time		
		for input_line in input_stream:
			height_map_line = [int(h) for h in input_line.strip()]
			height_map.append(height_map_line)

		return height_map


#returns True if the point is a minimum and all neighbour
#coords that are bigger
def isMinimum(height_map,i,j,h,w):

	isMin = True
	bigger_neighbours = []

	#if point is bigger than above return false
	if (i > 0):
		if (height_map[i][j] >= height_map[i - 1][j]):
			isMin = False
		else:
			bigger_neighbours.append((i-1,j))

	#if point if bigger than below return false
	if (i < (h-1)):
		if (height_map[i][j] >= height_map[i + 1][j]):
			isMin =  False
		else:
			bigger_neighbours.append((i+1,j))

	#if point is bigger than left return false
	if (j > 0):
		if (height_map[i][j] >= height_map[i][j - 1]):
			isMin =  False
		else:
			bigger_neighbours.append((i,j-1))

	#if point if bigger than right return false
	if (j < (w-1)):
		if (height_map[i][j] >= height_map[i][j + 1]):
			isMin =  False
		else:
			bigger_neighbours.append((i,j+1))

	#otherwise it is a min
	return isMin, bigger_neighbours


def find_all_mins(height_map):

	height = len(height_map)
	width = len(height_map[0])
	
	minimums = []
	for i in range(height):
		for j in range(width):

			isMin, _ = isMinimum(height_map,i,j,height,width)
			if isMin:
				minimums.append((i,j))

	return minimums

	
def calc_risk_level(height_map, minimums):
	
	risk_level = sum([height_map[i][j] + 1 for i,j in minimums])
	
	return risk_level


#breadth first search to find basin
def basin_BFS(height_map, minimum):

	height = len(height_map)
	width = len(height_map[0])

	visited = set()	
	
	frontier = deque()
	frontier.append(minimum)

	#when this is done visited will be the basin coordinates
	while len(frontier) > 0:

		#get the new point to visit
		point = frontier.popleft()
		
		#add it to the list of visited points
		visited.add(point)

		#get the larger neighbours of the point
		i,j = point
		_, bigger_neighbours = isMinimum(height_map,i,j,height,width)

		#add the neighbours to the frontier if they are new and < 9
		for n_point in bigger_neighbours:
			
			n_i, n_j = n_point		

			if (height_map[n_i][n_j] < 9) and (n_point not in visited):
				frontier.append(n_point)

	return visited


def find_all_basins(height_map, minimums):

	basins = []

	for minimum in minimums:
		basin = basin_BFS(height_map, minimum)
		basins.append(basin)

	return basins


def calc_basin_risk_level(basins):
	
	risk_level = sorted([len(basin) for basin in basins])
	risk_level = risk_level[-1]*risk_level[-2]*risk_level[-3]
	
	return risk_level


height_map = load_stuff("input9.txt")
minimums = find_all_mins(height_map)
risk_level = calc_risk_level(height_map, minimums)
print(risk_level)
basins = find_all_basins(height_map, minimums)
basin_risk_level = calc_basin_risk_level(basins)
print(basin_risk_level)

