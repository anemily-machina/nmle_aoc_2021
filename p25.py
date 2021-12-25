import io
import time


"""
Logic.. just do it?
"""


"""
loading handles part 1 and part 2
as well as loading any starting state for debugging
"""
def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		input_data = []
		for input_line in input_stream:
			input_data.append(input_line.strip())


		marina_trench = MarinaTrench(len(input_data), len(input_data[0]))

		for x, input_line in enumerate(input_data):

			for y, floor in enumerate(input_line):

				if floor == '>':
					marina_trench.add_right_sea_cucumber(x,y)

				elif floor == 'v':
					marina_trench.add_down_sea_cucumber(x,y)

		marina_trench.finalize_sea_floor()

		return marina_trench



class MarinaTrench():

	def __init__(self, height, width):

		self.height = height
		self.width = width

		self.moving_right_sea_cucumbers = set([])
		self.moving_down_sea_cucumbers = set([])

		self.sea_floor = [['.' for _ in range(self.width)] for _ in range(self.height)]


	def add_right_sea_cucumber(self, x, y):
		self.sea_floor[x][y] = '>'

	
	def add_down_sea_cucumber(self, x, y):
		self.sea_floor[x][y] = 'v'

	
	def finalize_sea_floor(self):
		for x in range(self.height):
			for y in range(self.width):
				
				if self.sea_floor[x][y] == '>':
					nx,ny = self._get_right(x,y)

					if self.sea_floor[nx][ny] == '.':
						self.moving_right_sea_cucumbers.add((x,y))

				elif self.sea_floor[x][y] == 'v':
					nx,ny = self._get_down(x,y)

					if self.sea_floor[nx][ny] == '.':
						self.moving_down_sea_cucumbers.add((x,y))


	def _get_right(self, x, y):
		y = y + 1 if (y + 1 < self.width) else 0
		return x, y


	def _get_left(self, x, y):
		y = y - 1 if (y - 1 > -1) else (self.width - 1)
		return x, y


	def _get_down(self, x, y):
		x = x + 1 if (x + 1 < self.height) else 0
		return (x,y)


	def _get_up(self, x, y):
		x = x - 1 if (x - 1 > -1) else (self.height - 1)
		return x, y


	def do_step(self):		

		if (len(self.moving_right_sea_cucumbers) == 0) and (len(self.moving_down_sea_cucumbers) == 0):
			return False

		moved_right = self._do_right_steps()
		moved_down = self._do_down_steps()

		return True


	def _do_right_steps(self):

		next_moving_right_sea_cucumbers = set([])
		for x,y in self.moving_right_sea_cucumbers:

			#check if we are freeing up the left
			lx,ly = self._get_left(x,y)
			if self.sea_floor[lx][ly] == '>':
				next_moving_right_sea_cucumbers.add((lx,ly))

			#check if we are freeing up the up
			ux,uy = self._get_up(x,y)
			if self.sea_floor[ux][uy] == 'v':
				self.moving_down_sea_cucumbers.add((ux,uy))

			#move out of the space
			self.sea_floor[x][y] = '.'

			#move into the next position
			nx,ny = self._get_right(x,y)
			self.sea_floor[nx][ny] = '>'

			#check if we are blocking the new up
			ux,uy = self._get_up(nx,ny)
			if self.sea_floor[ux][uy] == 'v':
				self.moving_down_sea_cucumbers.remove((ux,uy)) #it should be here

			#check that we are not now blocked
			rx,ry = self._get_right(nx,ny)
			if self.sea_floor[rx][ry] == '.':
				next_moving_right_sea_cucumbers.add((nx,ny))

		self.moving_right_sea_cucumbers = next_moving_right_sea_cucumbers


	def _do_down_steps(self):

		next_moving_down_sea_cucumbers = set([])
		for x,y in self.moving_down_sea_cucumbers:

			#check if we are freeing up the left
			lx,ly = self._get_left(x,y)
			if self.sea_floor[lx][ly] == '>':
				self.moving_right_sea_cucumbers.add((lx,ly))

			#check if we are freeing up the up
			ux,uy = self._get_up(x,y)
			if self.sea_floor[ux][uy] == 'v':
				next_moving_down_sea_cucumbers.add((ux,uy))

			#move out of the space
			self.sea_floor[x][y] = '.'

			#move into the next position
			nx,ny = self._get_down(x,y)
			self.sea_floor[nx][ny] = 'v'

			#check if we are blocking the new left
			lx,ly = self._get_left(nx,ny)
			if self.sea_floor[lx][ly] == '>':
				self.moving_right_sea_cucumbers.remove((lx,ly)) #it should be here

			#check that we are not now blocked
			dx,dy = self._get_down(nx,ny)
			if self.sea_floor[dx][dy] == '.':
				next_moving_down_sea_cucumbers.add((nx,ny))

		self.moving_down_sea_cucumbers = next_moving_down_sea_cucumbers	


	def print(self):
		output = ''
		for x in range(self.height):
			for y in range(self.width):
				output += self.sea_floor[x][y]
			output += '\n'				
		print(output)
		print("right",self.moving_right_sea_cucumbers)
		print("down",self.moving_down_sea_cucumbers)


def when_can_I_land(marina_trench):

	count = 0
	can_land = False
	while not can_land:
		if count == 453:
			print('still wrong')
		can_land = not marina_trench.do_step()		
		count+=1
	return count	
		

start_time = time.time()

fname = "input25.txt"
#fname = "easy25.txt"
#fname = "test25.txt" #don't set it to this, "Why isn't it stopping.. 3 hours later... oh..."

marina_trench = load_stuff(fname)
number_steps = when_can_I_land(marina_trench)
print(number_steps)


end_time = time.time()
print(round(end_time-start_time, 4))
