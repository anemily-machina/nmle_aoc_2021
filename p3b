import io
import copy

def binary2int(binary):
	mul = 1
	value = 0
	#read the list right to left
	for b in binary[::-1]:
		value += b*mul
		mul *= 2

	return value


def split(values, index, split_type):

	if(len(values) == 1):
		return(values)
	
	zeros = []
	ones = []

	#split set based on bit
	for i,v in enumerate(values):
		if v[index] == 0:
			zeros.append(i)
		else:
			ones.append(i)

	good_i = ones		
	#this can be one statement but w/e
	if (len(zeros) > len(good_i)) and (split_type == "most"):
		good_i = zeros
	elif (len(zeros) <= len(good_i)) and (split_type =="least"):
		good_i = zeros

	return [values[i] for i in good_i]


fname = "input3.txt"
with io.open(fname, 'r', encoding='utf-8') as input_stream: 
	
	#load all values
	binary_values = []	
	for line in input_stream:
		binary_values.append([int(c) for c in line[:-1]])

	diagnostics = []
	for split_type in ["most", "least"]:
		
		values_copy = copy.deepcopy(binary_values)
		
		for index in range(len(values_copy[0])):
			values_copy = split(values_copy, index, split_type)

		diagnostics.append(binary2int(values_copy[0]))
	
	print(diagnostics[0]*diagnostics[1])
