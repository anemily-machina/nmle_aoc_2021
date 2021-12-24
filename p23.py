import io
import time


"""
Logic

Do hallways moves first: frees up the hallway for other moves, puts amphipod in correct place

Then do room to room moves: doesn't clutter hallway, puts amphipod in correct place, frees up bad rooms

The try room to hallways moves: these suck as they clutter hallways, but they do free up rooms

You can probably choose r->h moves smartly or something but I don't
"""

class BurrowRoom():

	def __init__(self, hallway_pos, amph_type, starting_amphipods, top, done):

		self.pos = hallway_pos
		self.amph_type = amph_type		
		self.amphipods = starting_amphipods		
		self.top = top

		self.length = len(self.amphipods)		

		self._done = done


	def move_out(self):		

		steps = self.length - self.top
		amph_type = self.amphipods[self.top]
		self.amphipods[self.top] = -1
		self.top -= 1

		return steps, self.pos, amph_type


	def move_in(self):
		
		self.top += 1
		steps = self.length - self.top
		self.amphipods[self.top] = self.amph_type		

		#we are done if we added the top correct amphipod
		self._done = (self.top == (self.length - 1))
		
		return steps, self.pos, -1


	"""
	returns true if the room is move-out-able, and the ampipod that would move in
	"""
	def can_moveout(self):
		
		if self._done:
			return False, None, None

		#if we are not done, then if you can't move in the top amphipod can move out
		return (not self.can_movein()), self.pos, self.amphipods[self.top]


	"""
	returns true if the room is move-in-able
	"""
	def can_movein(self):

		#can't move into a room that is full of the correct amphipods
		if self._done:
			return False

		curr_pos = self.top
		while (curr_pos > -1) and (self.amphipods[curr_pos] == self.amph_type):
			curr_pos -= 1

		#if all the existing amphipods are the correct type you can move in
		if curr_pos == -1:
			return True

		#otherwise atleast one is bad so no one can move in yet
		return False


	def isDone(self):		
		return self._done


	def copy(self):
		starting_room = self.amphipods.copy()
		return BurrowRoom(self.pos, self.amph_type, starting_room, self.top, self._done)


class BurrowHallway():

	def __init__(self, starting_hallway, standing_positions):

		self.hallway = starting_hallway
		self.length = len(self.hallway)
		self.standing_positions = standing_positions


	def move(self, starting_position, ending_position):

		#swap hallway positions
		self.hallway[starting_position], self.hallway[ending_position] = self.hallway[ending_position], self.hallway[starting_position]

		return abs(ending_position - starting_position)


	def can_move(self, starting_position, ending_position):

		range_start = (starting_position + 1) if (starting_position < ending_position) else (starting_position - 1)
		range_end = ending_position

		range_start, range_end = min([range_start, range_end]), max([range_start, range_end]) + 1

		for h in self.hallway[range_start:range_end]:
			if h > -1:
				return False

		return True


	def get_valid_h2h_endings(self, starting_position):
		valid_h2h_endings = []
		for pos in self.standing_positions:
			if pos != starting_position:
				if self.can_move(starting_position, pos):
					valid_h2h_endings.append(pos)
		return valid_h2h_endings


	def get_amphipods(self):
		h_amphipods = []
		for h_pos, amph_type in enumerate(self.hallway):
			if amph_type > -1:
				h_amphipods.append([h_pos, amph_type])
		return h_amphipods


	def copy(self):
		starting_hallway = self.hallway.copy()
		return BurrowHallway(starting_hallway, self.standing_positions)


class Burrow():

	def __init__(self, hallway, rooms, cost=0):

		self.hallway = hallway
		self.rooms = rooms
		self.cost = cost


	"""
	Returns a list of valid moves (if we are not done)

	Case1: an amphipod can move from the hallway into it's correct room
	Returns: list with only that move

	Case2: an amphipod can move from it's current room into it's correct room
	Returns: list with only that move

	Case3: not case1 or case 2 and there exists at least 1 valid room->hallway move
	Returns: list of all valid moves from room to hallways positions

	case4: none of the above
	returns None
	"""
	def get_valid_moves(self):	

		moves = self._get_valid_h2r_moves()

		if moves is not None:
			return [moves]

		moves = self._get_valid_r2r_moves()

		if moves is not None:
			return [moves]

		moves = self.get_valid_r2h_moves()

		if len(moves) > 0:
			return moves

		return None


	def do_valid_moves(self, moves):

		new_hallway = self.hallway.copy()
		new_rooms = []
		for room in self.rooms:
			new_rooms.append(room.copy())

		amph_type = moves[0]		
		cost_per_step = 10 ** amph_type
		steps = 0

		for move in moves[1:]:

			move_type = move[0]

			if move_type == 'h2h':
				move_start, move_end = move[1], move[2]
				move_steps = new_hallway.move(move_start, move_end)

			elif move_type == 'h2r':
				room = new_rooms[move[1]]
				move_steps, room_position, amph_type = room.move_in()
				new_hallway.hallway[room_position] = amph_type

			elif move_type == 'r2h':
				room = new_rooms[move[1]]
				move_steps, room_position, amph_type = room.move_out()
				new_hallway.hallway[room_position] = amph_type

			steps += move_steps

		new_cost = self.cost + steps*cost_per_step

		return Burrow(new_hallway, new_rooms, new_cost)


	def _get_valid_h2r_moves(self):

		#get the amphipods in the hallways
		hallway_amphipods = self.hallway.get_amphipods()

		#check if each hallway amphipod can enter it's correct room
		for h_pos, amph_type in hallway_amphipods:

			#check if we can even move infront of the correct room and the room is open to move in
			amph_room = self.rooms[amph_type]
			if self.hallway.can_move(h_pos, amph_room.pos) and amph_room.can_movein():

				move1 = ('h2h', h_pos, amph_room.pos)
				move2 = ('h2r', amph_type)

				return [amph_type, move1, move2]

		return None


	def _get_valid_r2r_moves(self):

		#check for each room if the top amphipod can move out
		for room_id, room in enumerate(self.rooms):

			can_moveout, hallway_pos, amph_type = room.can_moveout()

			#if the top amphipod can move out, see if it can make it to the correct room
			if can_moveout:
			
				amph_room = self.rooms[amph_type]
				if self.hallway.can_move(room.pos, amph_room.pos) and amph_room.can_movein():

					move1 = ('r2h', room_id)
					move2 = ('h2h', room.pos, amph_room.pos)
					move3 = ('h2r', amph_type)

					return [amph_type, move1, move2, move3]


	def get_valid_r2h_moves(self):

		valid_r2h_moves = []

		#check for each room if the top amphipod can move out
		for room_id, room in enumerate(self.rooms):

			can_moveout, hallway_pos, amph_type = room.can_moveout()

			#if the top amphipod can move out, see if it can make it to the correct room
			if can_moveout:

				move1 = ('r2h', room_id)

				h2h_endings = self.hallway.get_valid_h2h_endings(hallway_pos)

				for h2h_end in h2h_endings:

					move2 = ('h2h', room.pos, h2h_end)

					valid_r2h_moves.append([amph_type, move1, move2])

		return valid_r2h_moves


	def isDone(self):
		for room in self.rooms:
			if not room.isDone():
				return False
		return True


	def get_hashable(self):
		hashable = []
		hashable += self.hallway.hallway
		for room in self.rooms:
			hashable += room.amphipods
		hashable = tuple(hashable)
		return hashable


	def print(self):
		print(self.cost)
		print(self.hallway.hallway)
		for room in self.rooms:
			print(room.amphipods)
		print()


class GoodBurrowMaker():

	def __init__(self, burrow):

		self.starting_burrow = burrow
		self._least_energy_burrow = None

		self._burrow_dict = {}


	def least_energy_burrow(self):

		if self._least_energy_burrow is None:
			self._find_least_energy_burrow_recursive([self.starting_burrow])

		return self._least_energy_burrow[-1]


	def _find_least_energy_burrow_recursive(self, burrows):

		curr_burrow = burrows[-1]		

		#check if we have seen this burrow state with a lower cost or update the burrow dict if we haven't
		burrow_hashable = curr_burrow.get_hashable()
		if (burrow_hashable not in self._burrow_dict) or (self._burrow_dict[burrow_hashable] > curr_burrow.cost):
			self._burrow_dict[burrow_hashable] = curr_burrow.cost
		else:
			return

		#if the burrow is done check if it took less energy
		if curr_burrow.isDone():	
			if (self._least_energy_burrow is None) or (self._least_energy_burrow[-1].cost > curr_burrow.cost):
				self._least_energy_burrow = burrows
			return

		#cost is always increasing, if this search path is already too expensive prune it
		if (self._least_energy_burrow is not None) and (curr_burrow.cost >= self._least_energy_burrow[-1].cost):
			return

		#otherwise we are in a burrow state we have not seen with a lower cost
		#and we are not done with this burrow
		#and we are not more expernsive than the smallest cost found so far
		valid_moves = curr_burrow.get_valid_moves()

		if valid_moves is None:
			return			

		for valid_move_set in valid_moves:

			new_burrow = curr_burrow.do_valid_moves(valid_move_set)

			self._find_least_energy_burrow_recursive(burrows + [new_burrow])


	#for debuggin
	def print_best(self):

		if self._least_energy_burrow is None:
			print("run find")
			return

		for burrow in self._least_energy_burrow:			
			burrow.print()

"""
loading handles part 1 and part 2
as well as loading any starting state for debugging
"""
def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		input_stream.readline()

		alpha2num = {'.':-1,'A':0,'B':1,'C':2,'D':3}

		#initialize the hallway items (we will prune standing positions later)
		starting_hallway = [alpha2num[h] for h in input_stream.readline().strip()[1:-1]]
		standing_positions = [i for i in range(len(starting_hallway))]
		

		#set up room input based on which part we are doing
		room_size = 2 if part == 1 else 4

		rooms = [[-1 for _ in range(room_size)] for _ in range(4)]

		room_input = []

		for input_line in input_stream:
			room_input.append(input_line.strip())

		room_input = room_input[:-1]

		if part == 2:
			new_1 = "  #D#C#B#A#"
			new_2 = "  #D#B#A#C#"
			room_input = [room_input[0], new_1, new_2, room_input[1]]

		room_input = room_input[::-1]
		

		room2pos = [2,4,6,8]

		for room_j, room_line in enumerate(room_input):

			room_i = 0

			for char in room_line:

				if char in alpha2num:
					rooms[room_i][room_j] = alpha2num[char]
					room_i += 1

		#make the burrow rooms index = room_type
		starting_rooms = []
		for amph_type, starting_amphipods in enumerate(rooms):

			#find the top of the starting list
			top = len(starting_amphipods) - 1
			while (top > -1) and (starting_amphipods[top] == -1):
				top -=1

			#check 
			done = (top == (len(starting_amphipods) - 1))
			curr_pos = top
			while done and (curr_pos > -1):
				done = done and (starting_amphipods[curr_pos] == amph_type)
				curr_pos -= 1

			new_room = BurrowRoom(room2pos[amph_type], amph_type, starting_amphipods, top, done)
			starting_rooms.append(new_room)
			standing_positions.remove(room2pos[amph_type])

		#make the hallway
		burrow_hallway = BurrowHallway(starting_hallway, standing_positions)
		burrow = Burrow(burrow_hallway, starting_rooms)

		return burrow


start_time = time.time()

fname = "input23.txt"
#fname = "easy23.txt"
#fname = "test23.txt"


starting_burrow = load_stuff(fname, 1)
good_burrow_maker = GoodBurrowMaker(starting_burrow)
best_burrow = good_burrow_maker.least_energy_burrow()
print(best_burrow.cost)


starting_burrow = load_stuff(fname, 2)
good_burrow_maker = GoodBurrowMaker(starting_burrow)
best_burrow = good_burrow_maker.least_energy_burrow()
print(best_burrow.cost)


end_time = time.time()
print(round(end_time-start_time, 4))
