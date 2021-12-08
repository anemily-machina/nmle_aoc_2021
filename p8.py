import io

def load_stuff(fname):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		all_commands = []
		all_outputs = []
		for input_line in input_stream:
			
			commands, outputs = input_line.strip().split(' | ')
			
			commands = [set(c) for c in commands.strip().split()]
			outputs = ["".join(sorted(o)) for o in outputs.strip().split()]

			all_commands.append(commands)
			all_outputs.append(outputs)		

		return all_commands, all_outputs


def count_by_lengths(all_patterns, lengths):

	count = 0
	for patterns in all_patterns:	
		for p in patterns:
			if len(p) in lengths:
				count += 1

	return count


"""
are we supposed to program some fancy algorithm that does this or make the logic by hand/brain?
"""
def decode_all_outputs(all_commands, all_outputs):

	total_value = 0
	for commands, outputs in zip(all_commands, all_outputs):
		output_value = decode_output(commands, outputs)
		total_value += output_value

	return total_value


def decode_output(commands, outputs):

	known_c = {}	

	#decode the easy ones first 1,4,7,8
	for i in range(len(commands)-1,-1, -1):
		c = commands[i]
		if len(c) == 2:
			known_c[1] = commands.pop(i)
		elif len(c) == 4:
			known_c[4] = commands.pop(i)
		elif len(c) == 3:
			known_c[7] = commands.pop(i)
		elif len(c) == 7:
			known_c[8] = commands.pop(i)

	#decode 3,5,2
	for i in range(len(commands)-1,-1, -1):
		c = commands[i]
		if len(c) == 5:
			#3 and 1 have an intersetcion of 2, 5/2 and 1 have an intersection of 1
			if len(c.intersection(known_c[1]))==2:
				known_c[3] = commands.pop(i)
			#otherwise it is 2 or 5.
			# 5 int 4 = 3, 2 int 4 = 2
			elif len(c.intersection(known_c[4]))==3:
				known_c[5] = commands.pop(i)
			#otherwise it must be 2
			else:
				known_c[2] = commands.pop(i)

	#decode 0,6,9 (nice)
	for i in range(len(commands)-1,-1, -1):
		c = commands[i]
		#9 and 3 have intersection 5 (as opposed to 4)
		if len(c.intersection(known_c[3]))==5:
			known_c[9] = commands.pop(i)
		#between 6 and 0, only 0 has intersection 2 with 1
		elif len(c.intersection(known_c[1]))==2:
			known_c[0] = commands.pop(i)
		#only 6 remains
		else:
			known_c[6] = commands.pop(i)

	#flip dictionary
	known_c = {"".join(sorted(list(known_c[key]))):key for key in known_c}

	#calculate the output value
	output_value = [str(known_c[c]) for c in outputs]
	output_value = int("".join(output_value))

	return output_value

	

all_commands, all_outputs = load_stuff("input8.txt")
num1478 = count_by_lengths(all_outputs, [2,4,3,7])
print(num1478)
total_value = decode_all_outputs(all_commands, all_outputs)
print(total_value)


