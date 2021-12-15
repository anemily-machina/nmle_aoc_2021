import io
import heapq

def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		cave_graph_weights = []

		repeat = 1 if part == 1 else 5
		for input_line in input_stream:
			
			cave_graph_weights_line = [int(c) for c in input_line.strip() ]			
			
			original_width = len(cave_graph_weights_line)
			for r in range(1,repeat):
				line_extension = [(c+1) if (c+1) < 10 else 1 for c in cave_graph_weights_line[original_width*(r-1):original_width*r]]	
				cave_graph_weights_line+=line_extension			

			cave_graph_weights.append(cave_graph_weights_line)

		original_height = len(cave_graph_weights)
		for r in range(1,repeat):
			for i in range(0, original_height):
				cave_graph_weights_line = [(c + 1) if (c + 1) < 10 else 1 for c in cave_graph_weights[i+(r-1)*original_height] ]	
				cave_graph_weights.append(cave_graph_weights_line)

		cave_h = len(cave_graph_weights)
		cave_w = len(cave_graph_weights[0])
		cave_count = cave_h*cave_w

		vertex2edge = {}

		for i in range(cave_count):
			x = i // cave_w
			y = i % cave_w

			vertex2edge[i] = []

			adjacent_vertexes = get_adjacent(x,y,cave_h, cave_w, False)
			
			for v_x, v_y in adjacent_vertexes:
				vertex2edge[i].append((cave_graph_weights[v_x][v_y], i, v_x*cave_w + v_y))

		return vertex2edge


def get_adjacent(i,j,h,w,diag=False):	

	#calculate offsets
	coords = []
	for offset in [-1,1]:
		c_j = j+offset
		if (c_j > -1) and (c_j < w):
			coords.append((i, c_j))
		c_i = i+offset
		if (c_i > -1) and (c_i < h):
			coords.append((c_i, j))
	if diag:
		for offset_i in [-1,1]:
			for offset_j in [-1,1]:	
				c_i = i+offset
				c_j = j+offset
				if (c_i > -1) and (c_i < h) and (c_j > -1) and (c_j < w):
					coords.append((c_i, c_j))

	return coords


"""
The input is essentially a weighted graph where edge weights are the
risk level, thus we want to find the shortest path from 0,0 to the bottom right

Find minimum spanning tree from a point (0,0), follow path backwards from the end point

yes this finds the shortest path from 0,0 to all points w/e

use heapq to do priority queue
"""
def find_min_spanning_tree(vertex2edge, start, target=None):

	tree_vertexes = set([start])
	tree_edges = set()
	cloud_edges = vertex2edge[start]
	heapq.heapify(cloud_edges)

	#number of edges in a minimal spanning tree is |V|-1
	while len(tree_vertexes) < len(vertex2edge):

		next_edge = heapq.heappop(cloud_edges)

		#edge is (c,i,j) where edge is i->j with cost c
		next_cost,_,next_vertex = next_edge

		#if the vertex has already been added ignore this edge
		if next_vertex in tree_vertexes:
			continue

		tree_vertexes.add(next_vertex)
		tree_edges.add(next_edge)

		if (target is not None) and (next_vertex == target):
			return tree_edges

		for c,i,j in vertex2edge[next_vertex]:
			if j not in tree_vertexes:
				 heapq.heappush(cloud_edges, (c+next_cost,i,j))

	return tree_edges


def find_path_cost(tree_edges, end):

	for c,i,j in tree_edges:
		if j == end:
			return c
			
	
fname = "input15.txt"
vertex2edge = load_stuff(fname, 1)
min_tree_edges = find_min_spanning_tree(vertex2edge, 0, len(vertex2edge) - 1)
cost = find_path_cost(min_tree_edges, len(vertex2edge) - 1)
print(cost)

vertex2edge = load_stuff(fname, 2)
min_tree_edges = find_min_spanning_tree(vertex2edge, 0, len(vertex2edge) - 1)
cost = find_path_cost(min_tree_edges, len(vertex2edge) - 1)
print(cost)
