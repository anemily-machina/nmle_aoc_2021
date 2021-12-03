import io

fname = "input2.txt"
with io.open(fname, 'r', encoding='utf-8') as input_stream: 
	forward = 0
	depth = 0
	aim = 0

	for line in input_stream:
		command, value = line.split()

		if command == 'forward':			
			forward += int(value)
			depth += aim*int(value)
		elif command == "down":
			aim += int(value)
		elif command == "up":
			aim -= int(value)

	print(forward*depth)

	
