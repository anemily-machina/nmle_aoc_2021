import io

fname = "p1A.txt"
with io.open(fname, 'r', encoding='utf-8') as input_stream: 
	count = 0
	
	window = []
	for _ in range(3):
		window.append(int(input_stream.readline()))

	for line in input_stream:
		window.append(int(line))		
		count += 1 if sum(window[1:4]) > sum(window[0:3]) else 0
		window.pop(0)

	print(count)
