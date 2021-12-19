import io
import numpy as np
import time

"""
Brute Force :D
"""

#keeps track 
class Scanner():

	_rotation_matricies = None

	@classmethod
	def check_alignment(cls, new_scanner, aligned_scanner):

		count = 0

		#iterate through all the rotations of the beacons
		for rotated_beacons, rotation_matrix in Scanner._rotated_beacon_iterator(new_scanner):			

			new_origin = Scanner._check_roatated_alignment(rotated_beacons, aligned_scanner.beacons)

			if new_origin is not None:
				return rotation_matrix, new_origin

		return None, None


	"""
	brute force check each beacon from one set as a matching each beacon from the other set
	If intersection is >= 12 then they are aligned at that beacon

	if the number of rotated beacons left to check is < 12 we can stop (if there was a match some
	beacon we already checked would be have created an alignement)
	"""
	@classmethod	
	def _check_roatated_alignment(cls, rotated_beacons, aligned_beacons):		

		aligned_beacons_set = set([(x,y,z) for x,y,z in aligned_beacons])

		rbi = len(rotated_beacons) - 1		

		#while there are at least 12 beacons left that are possibly aligned
		while rbi > 10:

			current_rotated_beacon = rotated_beacons[rbi]

			#check if the current beacon is any of the aligned beacons

			for aligned_beacon in aligned_beacons: 
			
				curr_offset = current_rotated_beacon - aligned_beacon

				offset_rotated_beacons = rotated_beacons - curr_offset

				offset_rotated_beacons_set = set([(x,y,z) for x,y,z in offset_rotated_beacons])

				new_aligned_beacons_set = aligned_beacons_set.intersection(offset_rotated_beacons_set)

				#if there is alignement calculate the origin of the new scanner
				if len(new_aligned_beacons_set) >= 12:
					new_origin = -curr_offset
					return new_origin

			rbi -= 1		


	@classmethod
	def _rotated_beacon_iterator(cls, scanner):

		if Scanner._rotation_matricies is None:
			Scanner._generate_rotation_matricies()

		beacons = scanner.beacons

		for rotation_matrix in Scanner._rotation_matricies:

			yield np.matmul(beacons, rotation_matrix), rotation_matrix


	#only 24 of these are unique
	@classmethod
	def _generate_rotation_matricies(cls):

		rotation_matricies = []

		for i in range(4):

			r1 = Scanner._fixed_axis_rotation('x', i)

			for j in range(4):

				r2 = Scanner._fixed_axis_rotation('y', j)

				for k in range(4):

					r3 = Scanner._fixed_axis_rotation('z', k)

					r = np.matmul(r1,r2)
					r = np.matmul(r,r3)

					rotation_matricies.append(r)

		rotation_matricies = np.array(rotation_matricies)
		rotation_matricies = np.unique(rotation_matricies, axis = 0)
		Scanner._rotation_matricies = rotation_matricies		


	@classmethod
	def _fixed_axis_rotation(cls, rotation_axis, angle):

		cos = [1,0,-1,0]
		sin = [0,1,0,-1]

		c = cos[angle]
		s = sin[angle]

		if rotation_axis == 'x':
			rotation_m = np.array([[1,0,0],[0,c,-s],[0,s,c]])

		elif rotation_axis == 'y':
			rotation_m = np.array([[c,0,s],[0,1,0],[-s,0,c]])

		elif rotation_axis == 'z':
			rotation_m = np.array([[c,-s,0],[s,c,0],[0,0,1]])

		return rotation_m


	def __init__(self, id):
		self.id = id
		self.pos = (0,0,0) #all scanners think they are at origin to start
		self.beacons = [] #scanner will be rotated so y is forward z is up x right after alignement


	def add_beacon(self, beacon):		
		self.beacons.append(beacon)


	def finalize_scan(self):
		self.beacons = np.array(self.beacons)


	def align(self, rotation_matrix, new_origin):

		self.beacons = np.matmul(self.beacons, rotation_matrix)
		self.beacons = self.beacons + new_origin
		self.pos = tuple(new_origin)


	def __str__(self):
		output = f'ID:{self.id}\npos:{self.pos}\nBeacons:\n{self.beacons}'
		return output


def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		scanners = []
		idnum = 0
		curr_scanner = None

		for input_line in input_stream:

			if input_line[:3] == "---":
				
				if curr_scanner is not None:
					curr_scanner.finalize_scan()
					scanners.append(curr_scanner)
				
				curr_scanner = Scanner(idnum)
				idnum += 1

			elif len(input_line.strip()) == 0:
				pass

			else:
				
				beacon = tuple([int(p) for p in input_line.strip().split(',')])
				curr_scanner.add_beacon(beacon)

		#add the last one
		curr_scanner.finalize_scan()
		scanners.append(curr_scanner)

	return scanners


def find_matches(scanners):

	#assume scanner 0 is at 0,0,0 forward=y, up=z, right=x
	aligned_scanners = [scanners.pop(0)]
	prev_aligned_scanners = aligned_scanners

	#until we have aligned all scanners
	while len(scanners) > 0:		

		#start at last scanner
		scanner_i = len(scanners) - 1
		next_aligned_scanners = []

		while scanner_i > -1:
			
			curr_scanner = scanners[scanner_i]

			#check if the current unaligned scanner is aligned with any newly aligned scanners
			#we don't need to recheck the against old ones
			asi = 0
			while asi < len(prev_aligned_scanners):

				curr_aligned_scanner = prev_aligned_scanners[asi]

				rotation_matrix, scanner_origin = Scanner.check_alignment(curr_scanner, curr_aligned_scanner)

				#if an alignment is found update the scanner position and the beacon positions
				if rotation_matrix is not None:
					
					curr_scanner.align(rotation_matrix, scanner_origin)
					next_aligned_scanners.append(scanners.pop(scanner_i))

					asi = len(prev_aligned_scanners)

				asi += 1

			scanner_i -= 1

		aligned_scanners += next_aligned_scanners
		prev_aligned_scanners = next_aligned_scanners

	return aligned_scanners


def count_beacons(scanners):

	all_beacons = set()

	for scanner in scanners:

		beacon_set = set([(x,y,z) for x,y,z in scanner.beacons])
		all_beacons = all_beacons.union(beacon_set)

	return list(all_beacons)


def find_largest_L1(scanners):
	
	largest_L1 = -float('inf')

	for i in range(len(scanners) - 1):

		x1,y1,z1 = scanners[i].pos

		for j in range(i+1, len(scanners)):

			x2,y2,z2 = scanners[j].pos

			L1 = abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

			if L1 > largest_L1:
				largest_L1 = L1

	return largest_L1


start_time = time.time()
fname = "input19.txt"
scanners = load_stuff(fname)
aligned_scanners = find_matches(scanners)
all_beacons = count_beacons(aligned_scanners)
print(len(all_beacons))
largest_distance = find_largest_L1(aligned_scanners)
print(largest_distance)
end_time = time.time()
print(round(end_time-start_time, 4))
