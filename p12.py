import io

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		connection_graph = {}		
		
		for input_line in input_stream:
			left, right = input_line.strip().split('-')
			
			if left not in connection_graph:
				connection_graph[left] = []

			if right not in connection_graph:
				connection_graph[right] = []

			connection_graph[left].append(right)
			connection_graph[right].append(left)
		
		return connection_graph 


def count_all_paths(connection_graph, visit_lower_once=False):
	
	path_count = 0

	path_stub = []
	path_stub.append('start')

	_, path_count = recusive_find_paths(connection_graph, path_stub, path_count, visit_lower_once)

	return path_count


def recusive_find_paths(connection_graph, path_stub, path_count, visit_lower_once):

	path_head = path_stub[-1]

	#if we are at the end of the cave increase the path count
	if path_head == 'end':		
		path_count += 1
		return path_stub, path_count

	#otherwise explore all check all connected branches
	new_branches = connection_graph[path_head]

	for branch in new_branches:

		path_stub.append(branch)

		#make sure we can take this path for free
		if (branch.isupper()) or (branch not in path_stub[:-1]):
						
			path_stub, path_count = recusive_find_paths(connection_graph, path_stub, path_count, visit_lower_once)

		#otherwise see if we can take the path through the small cave twice
		elif visit_lower_once and (branch != 'start'):

			path_stub, path_count = recusive_find_paths(connection_graph, path_stub, path_count, visit_lower_once=False)
		
		path_stub.pop()


	return path_stub, path_count


connection_graph = load_stuff("input12.txt")
number_paths = count_all_paths(connection_graph, visit_lower_once=False)
print(number_paths)
number_paths = count_all_paths(connection_graph, visit_lower_once=True)
print(number_paths)

