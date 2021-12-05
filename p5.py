import io

def load_stuff(fname, part):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 
		area_map = {}	

		for input_line in input_stream:
			
			x1,y1,x2,y2 = split_input_line(input_line)
			line = get_line(x1,y1,x2,y2, part)
			add_line_map(area_map, line)

		return area_map


def split_input_line(input_line):
	
	c1, _, c2 = input_line.strip().split()
	x1,y1 = [int(c) for c in c1.split(',')]
	x2,y2 = [int(c) for c in c2.split(',')]

	return x1,y1,x2,y2


def get_line(x1,y1,x2,y2, part=1):

	line = []
	if x1 == x2:
		line = [(x1,y) for y in list(range(min([y1,y2]), max([y1,y2]) + 1))]

	elif y1 == y2:		
		line = [(x,y1) for x in list(range(min([x1,x2]), max([x1,x2]) + 1))]

	elif part == 2:		
		
		xs = list(range(min([x1,x2]), max([x1,x2]) + 1))
		if x1 > x2:
			xs = xs[::-1]			
		
		ys = list(range(min([y1,y2]), max([y1,y2]) + 1))
		if y1 > y2:
			ys = ys[::-1]	

		line = [(x,y) for x,y in zip(xs,ys)]

	return line	


def add_line_map(area_map, line):

	for c in line:
		if c not in area_map:
			area_map[c] = 0
		area_map[c] +=  1


def count_danger(area_map):
	danger = 0
	for c in area_map:
		if area_map[c] > 1:
			danger +=1
	return danger


part = 2
area_map = load_stuff("input5.txt", part)
danger = count_danger(area_map)
print(danger)
