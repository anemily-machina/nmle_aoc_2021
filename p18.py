import io

"""
if feels like I sould be using a doubly linked list for this?
"""

class SnailNumberNode():

	#basic double sides linked list node with value
	def __init__(self, prev_node, next_node, value):

		self.prev_node = prev_node
		self.next_node = next_node
		self.value = value


	#is the value a number?
	def is_number(self):
		return isinstance(self.value, int)


	#print up to K nodes from left to right
	def print(self, K=None):
		
		curr_node = self
		k=1

		output = f'{curr_node.value}'
		curr_node = curr_node.next_node

		while (curr_node is not None) and ((K is None) or (k < K)):
			output += f' {curr_node.value}'
			curr_node = curr_node.next_node
			k+=1

		print(output)


	#print up to K nodes from right to left
	def print_b(self, K=None):
	
		curr_node = self
		k=1

		output = f'{curr_node.value}'
		curr_node = curr_node.prev_node

		while (curr_node is not None) and ((K is None) or (k < K)):
			output += f' {curr_node.value}'
			curr_node = curr_node.prev_node
			k+=1

		print(output)
	

class SnailNumber():

	#doubly linked list keep track of head and tail
	def __init__(self, head, tail):
		self.head = head
		self.tail = tail		

	#print it all
	def __str__(self):

		curr_node = self.head

		output = curr_node.value
		curr_node = curr_node.next_node

		while curr_node is not None:
			output += f' {curr_node.value}'
			curr_node = curr_node.next_node

		return output	


	#perform self = self + n as per AOC rules
	def add(self, n):
	
		#add [ at start of new number
		new_head = SnailNumberNode(None, self.head, '[')
		self.head.prev_node = new_head
		
		#add ] at end of new number
		new_tail = SnailNumberNode(n.tail, None, ']')
		n.tail.next_node = new_tail

		#join numbers in the middle
		self.tail.next_node = n.head
		n.head.prev_node = self.tail

		self.head = new_head
		self.tail = new_tail

		self._reduce()


	#reduce self so it is a valid snailnumber
	def _reduce(self):

		reduced = False

		while (not reduced):
			self._check_explosions()
			reduced = self._check_splits()


	#process explosions left to right
	#explosions cannot cause more explosions directly so we can check left to right for all of them
	def _check_explosions(self):

		curr_node = self.head
		depth = 0

		while curr_node is not None:

			curr_value = curr_node.value

			if curr_value == '[':
				depth += 1

			elif curr_value == ']':
				depth -= 1

			if depth == 5:
				curr_node = self._do_explosion(curr_node)
				depth -= 1
			
			curr_node = curr_node.next_node


	#does an explosion at node = '[' of the exploding pair [int1, int2]	
	def _do_explosion(self, node):		

		kept_prev = node.prev_node

		node = node.next_node
		x = node.value

		#find the next number to the left and add x to it		
		curr_node = kept_prev
		while curr_node is not None:
			if curr_node.is_number():
				curr_node.value += x
				curr_node = None
			else:
				curr_node = curr_node.prev_node

		node = node.next_node
		y = node.value

		# now at the ']' of the exploding pair [x,y]
		node = node.next_node
		kept_next = node.next_node

		#find the next number to the right and add y to it
		
		curr_node = kept_next
		while curr_node is not None:
			if curr_node.is_number():
				curr_node.value += y
				curr_node = None
			else:
				curr_node = curr_node.next_node

		#cut out the exploding term and replace it with a 0 node
		zero_node = SnailNumberNode(kept_prev, kept_next, 0)
		kept_prev.next_node = zero_node
		kept_next.prev_node = zero_node

		return zero_node


	#split the first number on the left that needs splitting if one exists
	def _check_splits(self):

		curr_node = self.head

		while curr_node is not None:

			if curr_node.is_number() and (curr_node.value > 9):

				self._do_split(curr_node)

				return False

			curr_node = curr_node.next_node

		return True


	def _do_split(self, node):

		value = node.value
		valueIsOdd = (value%2 == 1)

		kept_prev = node.prev_node
		kept_next = node.next_node

		#add new left [
		new_open = SnailNumberNode(kept_prev, None, '[')
		kept_prev.next_node = new_open

		new_x = SnailNumberNode(new_open, None, value//2)
		new_open.next_node = new_x

		new_y = SnailNumberNode(new_x, None, value//2 + (1 if valueIsOdd else 0))
		new_x.next_node = new_y

		new_closed = SnailNumberNode(new_y, kept_next, ']')
		new_y.next_node = new_closed
		kept_next.prev_node = new_closed


	#calculate the magnitude of a snailnumber
	def magnitude(self):

		length = 0
		curr_node = self.head
		while curr_node is not None:
			length + =1
			curr_node=curr_node.next_node

		return self._recursive_magnitude(self.head, self.tail, length)


	def _recursive_magnitude(self, head, tail, length):

		#base case int
		if length == 1:
			return head.value

		#recurise case
		#snail numbers are always pairs of snail numbers [X,Y]
		else:
			left_snail_number_head = head.next_node
			left_length = 1				
								
			#start at the left most [ of X or an integer. either X or Y must be compound
			curr_node = left_snail_number_head

			#case of [int, Y]
			if curr_node.is_number():
				left_snail_number_tail = left_snail_number_head
			
			#case of [X,Y] or [X,int] 
			else:
				depth = 1
				
				#find last ] of X
				while depth > 0:
					
					curr_node = curr_node.next_node
					curr_value = curr_node.value

					if curr_value == '[':
						depth += 1

					elif curr_value == ']':
						depth -= 1

					left_length += 1

				#curr_node is now the leftmost ] of X
				left_snail_number_tail = curr_node				

			x = self._recursive_magnitude(left_snail_number_head, left_snail_number_tail, left_length)

			#p sure this just handles both cases of [X,Y] or [X,int] since right_length is 1 or it isn't
			right_snail_number_head = curr_node.next_node
			right_snail_number_tail = tail.prev_node
			right_length = length - left_length - 2

			y = self._recursive_magnitude(right_snail_number_head, right_snail_number_tail, right_length)

		return 3*x + 2*y


	#thanks part 2
	def copy(self):

		copy_head = SnailNumberNode(None, None, self.head.value)

		copy_prev_node = copy_head
		copy_curr_node = None
		
		curr_node = self.head.next_node
		while curr_node is not None:

			copy_curr_node = SnailNumberNode(copy_prev_node, None, curr_node.value)
			copy_prev_node.next_node = copy_curr_node
			copy_prev_node = copy_curr_node

			curr_node = curr_node.next_node

		return SnailNumber(copy_head, copy_prev_node)


def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		numbers = []

		for input_line in input_stream:

			input_line = input_line.strip()

			head_node = None
			prev_node = None
			for c in input_line:
				if c != ',':
					value = None
					if c.isnumeric():
						value = int(c)
					else:
						value = c

					if head_node is None:
						head_node = SnailNumberNode(None, None, value)
						prev_node = head_node
					else:
						curr_node = SnailNumberNode(prev_node, None, value)
						prev_node.next_node = curr_node
						prev_node = curr_node
			
			numbers.append(SnailNumber(head_node, prev_node))

	return numbers
	

def add_all_numbers(numbers):

	copy_numbers = []
	for number in numbers:
		copy_numbers.append(number.copy())

	curr_number = copy_numbers[0]

	for next_number in copy_numbers[1:]:

		curr_number.add(next_number)

	return curr_number


def add_all_pairs(numbers):

	best_mag = -float('inf')
	for n1 in numbers:
		for n2 in numbers:

			c1 = n1.copy()
			c2 = n2.copy()

			c1.add(c2)

			mag = c1.magnitude()

			if mag > best_mag:
				best_mag = mag

	return best_mag


fname = "input18.txt"
numbers = load_stuff(fname)
addition_result = add_all_numbers(numbers)
magnitude = addition_result.magnitude()
print(magnitude)
bests_pair_magnitude = add_all_pairs(numbers)
print(bests_pair_magnitude)
