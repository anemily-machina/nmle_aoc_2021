import io
import time


"""
did part 1 brute force
doing part 2 with pie
pie too slow

removing areas as we add them instead

"""

class Cuboid():

	def __init__(self, ranges):

		self.ranges = ranges


	"""
	returns none if there is no intersecion between this cuboid and the range

	otherwise it returns the cuboids that make up the remaining volume with no intersection after
	removing the cuboid defined by the range
	"""
	def remove(self, ranges):	

		if isinstance(ranges, Cuboid):
			ranges = ranges.ranges

		#check if this cuboid intersects this range
		intersection_ranges = self._intersection(ranges)
		if intersection_ranges is None:
			return None

		#if an intersecion exists split the cuboid into 6 cuboids of the remining volume
		#there is maybe a smart way to do this but I will do it the one way

		x1,x2,y1,y2,z1,z2 = self.ranges
		rx1,rx2,ry1,ry2,rz1,rz2 = intersection_ranges
		
		bottom_cuboid = Cuboid([x1,x2,y1,y2,z1,rz1 - 1])
		top_cuboid = Cuboid([x1,x2,y1,y2,rz2 + 1,z2])

		middle_backwards_cuboid = Cuboid([x1,x2,y1,ry1-1,rz1,rz2])
		middle_forwards_cuboid = Cuboid([x1,x2,ry2+1,y2,rz1,rz2])

		middle_middle_left_cuboid = Cuboid([x1,rx1-1,ry1,ry2,rz1,rz2])
		middle_middle_right_cuboid = Cuboid([rx2+1,x2,ry1,ry2,rz1,rz2])

		new_cuboids = [bottom_cuboid,top_cuboid,middle_backwards_cuboid,middle_forwards_cuboid,middle_middle_left_cuboid,middle_middle_right_cuboid]

		#filter out no volume cubids
		c_i = len(new_cuboids) - 1
		while c_i > -1:
			if new_cuboids[c_i].size() == 0:
				new_cuboids.pop(c_i)
			c_i -= 1

		return new_cuboids


	"""
	if there is an intersection
	"""
	def _intersection(self, ranges):
		
		#find the intersecion if any exist
		intersection_ranges = []
		for i in range(3):
			c1 = self.ranges[i*2]
			c2 = self.ranges[i*2+1]
			r1 = ranges[i*2]
			r2 = ranges[i*2+1]

			#if the range is too far positive no intersection
			if r1 > c2:
				return None
			#if the range is too far negative no intersection
			elif r2 < c1:
				return None
			#otherwise there is an intersection on this axis
			else:
				intersection_ranges += [max([c1,r1]), min([c2,r2])]

		return intersection_ranges


	def size(self):
		
		total_size = 1
		for i in range(3):
			c1 = self.ranges[i*2]
			c2 = self.ranges[i*2+1]
			total_size *= (c2 - c1 + 1)
		
		return total_size


	def __str__(self):

		return f'{self.ranges}'



class Reactor():

	def __init__(self, initialization):
		self.cuboids = []
		self.initialization = initialization


	def do_reboot_step(self, reboot_step):

		reboot_action = reboot_step['action']
		ranges = reboot_step['ranges']

		#if we are initializing clip cubes
		if self.initialization:
			for i in range(3):
				ranges[i*2] = max([ranges[i*2], -50])
				ranges[i*2+1] = min([ranges[i*2+1], 50])

				if (ranges[i*2+1] - ranges[i*2]) <= 0:
					return

		#if it is an on cuboid
		if reboot_action == 'on':

			new_cuboid = Cuboid(ranges)

			#make sure the clipped volume is not 0
			self._add_cuboid(new_cuboid)			

			return

		#otherwise we are on an off step
		self._remove_area(ranges)


	"""
	removes existing cuboids from new area and then adds them to list of areas
	"""
	def _add_cuboid(self, cuboid):

		curr_cuboids = [cuboid]

		for existing_cuboid in self.cuboids:

			next_cuboids = []

			for curr_cuboid in curr_cuboids:

				split_cuboids = curr_cuboid.remove(existing_cuboid)

				if split_cuboids is None:

					next_cuboids.append(curr_cuboid)

				else:

					next_cuboids += split_cuboids

			curr_cuboids = next_cuboids

		self.cuboids += curr_cuboids


	def _remove_area(self, ranges):

		new_cuboids = []

		for cuboid in self.cuboids:
			
			split_cuboids = cuboid.remove(ranges)

			#if split_cuboids is None then there was no intersecion
			if split_cuboids is None: 
				new_cuboids.append(cuboid)
			
			#otherwise it is the list of cuboids after removing the current range
			else:				
				new_cuboids += split_cuboids

		self.cuboids = new_cuboids

    
	def size(self):

		total_size = sum([c.size() for c in self.cuboids])

		return total_size


def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		reboot_steps = []
		for input_line in input_stream:
			
			reboot_action, cuboid = input_line.strip().split(' ')
			ranges = cuboid.split(',')
			ranges = [int(r) for rang in ranges for r in rang[2:].split('..')]
			
			reboot_steps.append({'action':reboot_action, 'ranges':ranges})

		return reboot_steps


def do_reboot_steps(reboot_steps, initialization):

	reactor = Reactor(initialization)

	for reboot_step in reboot_steps:

		reactor.do_reboot_step(reboot_step)

	return reactor


start_time = time.time()

fname = "input22.txt"
#fname = "test22.txt"
reboot_steps = load_stuff(fname)
reactor = do_reboot_steps(reboot_steps, True)
print(reactor.size())

end_time = time.time()
print(round(end_time-start_time, 4))
