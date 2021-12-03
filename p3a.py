import io

def binary2int(binary):
	mul = 1
	value = 0
	#read the list right to left
	for b in binary[::-1]:
		value += b*mul
		mul *= 2

	return value

fname = "input3.txt"
with io.open(fname, 'r', encoding='utf-8') as input_stream: 
	
	count = 1
	partial_sums = [int(c) for c in input_stream.readline()[:-1]]
	
	for line in input_stream:
		count += 1
		partial_sums = [p+int(c) for p,c in zip(partial_sums, line[:-1])]
	
	count /= 2
	#find magority bits
	gamma = [1 if p > count else 0 for p in partial_sums]
	#could also do some math here as eps is the compliment of gamma
	eps = [1 if g == 0 else 0 for g in gamma]

	gamma = binary2int(gamma)
	eps = binary2int(eps)

print(gamma*eps)
