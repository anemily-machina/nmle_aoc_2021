import io

fname = "input1.txt"
with io.open(fname, 'r', encoding='utf-8') as input_stream: 
	count = 0
	prev = int(input_stream.readline())
	for line in input_stream:
		curr = int(line)
		count += 1 if curr > prev else 0
		prev = curr

	print(count)
