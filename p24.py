import io
import time


"""
Maybe I should have got more sleep

Logic is you don't have to recompute the first n-1 digits when checking all values of 1 to 9 for digit n

prune when you see the same register state at the same digit calculation

part2 improvement prune based only on registers that do not get overwritten

old results
65984919997939
11211619541713
631.4563

improvement results
65984919997939
11211619541713
593.971

woo a whole half minute saving /s

I assume you can do it faster with multithreading or some shit

"""

class ALU():

	def __init__(self, registers):		

		self._reg2idx = {'x':0, 'y':1, 'z':2, 'w':3}
		self.registers = registers.copy()		


	def run_program(self, instructions, program_input):

		for instruction in instructions:

			completed = self._do_instruction(instruction, program_input)

			if not completed:
				return None

		return self.registers


	def _do_instruction(self, instruction, program_input):

		instruction_type = instruction[0]
		target_register = self._reg2idx[instruction[1]]

		if instruction_type == 'inp':
			self.registers[target_register] = program_input
			return True

		a = self.registers[target_register]

		b = instruction[2]
		if b in self._reg2idx:
			b = self.registers[self._reg2idx[b]]
		else:
			b = int(b)

		if instruction_type == 'add':		
			self.registers[target_register] = a + b

		elif instruction_type == 'mul':
			self.registers[target_register] = a * b

		elif instruction_type == 'div':
			if b == 0:
				return False
			self.registers[target_register] = a // b

		elif instruction_type == 'mod':
			if (a < 0) or (b <= 0):
				return False
			self.registers[target_register] = a % b

		elif instruction_type == 'eql':
			self.registers[target_register] = 1 if (a == b) else 0

		return self.registers


class ModelNumberFinder():

	def __init__(self, digit_programs):

		self.digit_programs = digit_programs

		#these are the values that matter for pruning branches we have seen before at digit k
		self.keep_indexes = []
		reg2idx = {'x':0,'y':1,'z':2,'w':3}

		for program in digit_programs:
			
			ki = []
			
			_, reg = program[0]
			ignore_index = reg2idx[reg]

			for i in range(4):
				if i != ignore_index:
					ki.append(i)

			self.keep_indexes.append(ki)


	def find_model_number(self, part):
		
		self.seen_registers = {n:set([]) for n in range(len(digit_programs))}
		self.digit_range = range(9,0,-1) if part == 1 else range(1,10)

		starting_register = [0,0,0,0]
		starting_value = ''

		return self._find_model_number_recursive(starting_register, starting_value, 0)


	"""
	depth first search
	"""
	def _find_model_number_recursive(self, register, value, digit):

		#base case
		#if we have ran all the programs
		if(digit == len(self.digit_programs)):

			#if this is a valid model number
			if(register[2] == 0):
				return value
			#otherwise this model numeber is not valid
			else:
				return None

		keep_index = self.keep_indexes[digit]
		register_hash = tuple([register[i] for i in keep_index])

		#if we have seen this register hash at this digit already it
		#failed on a higher/lower number and the end register will be the same
		if register_hash not in self.seen_registers[digit]:
			self.seen_registers[digit].add(register_hash)
		else:
			return None

		digit_program = self.digit_programs[digit]
			
		#recursive case
		for i in self.digit_range:

			alu = ALU(register)
			
			next_register = alu.run_program(digit_program, i)

			#if there wasn't a runtime error
			if next_register is not None:							

				next_value = value + f'{i}'
				next_digit = digit + 1

				result = self._find_model_number_recursive(next_register, next_value, next_digit)

				if result is not None:
					return result

		return None


"""
loading handles part 1 and part 2
as well as loading any starting state for debugging
"""
def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 
		
		monad_program = []		

		for input_line in input_stream:
			
			program_line = tuple(input_line.strip().split(' '))
			monad_program.append(program_line)			

		digit_programs = []			
		digit_program = None
		for program_line in monad_program:
			if program_line[0] == "inp":
				if digit_program is not None:
					digit_programs.append(digit_program)
				digit_program = []

			digit_program.append(program_line)

		digit_programs.append(digit_program)

		return digit_programs


start_time = time.time()

fname = "input24.txt"
#fname = "easy24.txt"

digit_programs = load_stuff(fname)
mode_number_finder = ModelNumberFinder(digit_programs)

largest = mode_number_finder.find_model_number(1)
print(largest)

smallest = mode_number_finder.find_model_number(2)
print(smallest)


end_time = time.time()
print(round(end_time-start_time, 4))
