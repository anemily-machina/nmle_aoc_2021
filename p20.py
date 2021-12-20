import io
import numpy as np
import copy
import time


#keeps track 
class BinaryPicture():

	def __init__(self, picture_array, infinity=0):

		self.picture = np.array(picture_array)
		self.infinity = infinity


	def count_bright(self):

		if self.infinity == '1':
			return float('inf')

		bright_count = 0
		for row in self.picture:
			for pixel in row:
				if pixel == 1:
					bright_count += 1

		return bright_count


class ImageEnhancer():

	@classmethod
	def apply_algorithm(cls, picture, algorithm, steps):

		prev_array = copy.deepcopy(picture.picture)
		prev_infinity = picture.infinity

		for _ in range(steps):
			
			padded_array = ImageEnhancer._pad_array(prev_array, prev_infinity, 2)			
			next_array, next_infinity = ImageEnhancer._do_algorithm_step(padded_array, prev_infinity, algorithm)

			prev_array = next_array
			prev_infinity = next_infinity

		new_picture = BinaryPicture(prev_array, prev_infinity)

		return new_picture


	@classmethod
	def _pad_array(cls, picture_array, padding_value, padding_amount):

		padded_array = np.pad(picture_array, pad_width=padding_amount, mode='constant', constant_values=padding_value)
		return padded_array


	@classmethod
	def _do_algorithm_step(cls, picture_array, infinity, algorithm):

		next_array = np.zeros((len(picture_array) - 2, (len(picture_array[0]) - 2)), dtype=np.int8)
		
		#update picture array
		#iterate along the columns
		for j in range(len(next_array[0])):

			window = [picture_array[0][j:j+3],picture_array[0][j:j+3],picture_array[1][j:j+3]]

			for i in range(len(next_array)):

				#update the current window
				window.pop(0)
				window.append(picture_array[i+2][j:j+3])

				#calculate the algorithm pixel value
				binary_string = [b for row in window for b in row]
				alg_index = sum([b*(2**i) for i,b in enumerate(binary_string[::-1])])

				next_array[i][j] = algorithm[alg_index]

		#update infinity
		binary_string = [infinity for _ in range(9)]
		alg_index = sum([b*(2**i) for i,b in enumerate(binary_string[::-1])])
		next_infinity = algorithm[alg_index]

		return next_array, next_infinity	


def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		enhancement_algorithm = [0 if c == '.' else 1 for c in input_stream.readline().strip()]
		
		input_stream.readline()

		picture_array = []
		for input_line in input_stream:
			picture_array_line = [0 if c == '.' else 1 for c in input_line.strip()]
			picture_array.append(picture_array_line)
			
		picture = BinaryPicture(picture_array)

	return enhancement_algorithm, picture




start_time = time.time()

fname = "input20.txt"
#fname = "test20.txt"
enhancement_algorithm, picture = load_stuff(fname)

enchanced_picture = ImageEnhancer.apply_algorithm(picture, enhancement_algorithm, 2)
bright_enchanced_picture = enchanced_picture.count_bright()
print(bright_enchanced_picture)

enchanced_picture = ImageEnhancer.apply_algorithm(picture, enhancement_algorithm, 50)
bright_enchanced_picture = enchanced_picture.count_bright()
print(bright_enchanced_picture)


end_time = time.time()
print(round(end_time-start_time, 4))
