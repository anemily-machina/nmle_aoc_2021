import io
import copy
import time


class DiracDiceGame():

	def __init__(self, player_starts, die, game_end_value):

		#variables shared acrooss universes (if deterministic only ever 1 game so die is "shared")
		self.number_players = len(player_starts)
		self.die = die
		self.game_end_value = game_end_value

		self.current_player = 0	

		#initial game conditions
		#why do I have to tuple list sometimes?
		player_positions = tuple([player_starts[i] for i in range(self.number_players)])
		player_scores = tuple([0 for name in range(self.number_players)])

		starting_game = (player_positions, player_scores)

		#game state:number of games with that state
		self.ongoing_games = {starting_game:1}	
		self.completed_games = {}


	def do_turn(self):

		#if the game is over do nothing
		if self.games_over():			
			print ("Games are over.")
			return

		#get the sum of 3 die rolls (either deterministic or quantum)
		#retult is dicitonary roll_value:number of universes with that roll
		rolls = self.die.roll_die(3)

		#store the game states after this roll
		next_game_states = {}

		for roll_value in rolls:

			roll_value_dimension_count = rolls[roll_value]

			for game_state in self.ongoing_games:
				
				#calculat the new number of dimensions that will have this gamestate from this roll and gamestate				
				game_state_dimension_count = self.ongoing_games[game_state]
				next_state_dimension_count = roll_value_dimension_count * game_state_dimension_count

				#extract the gamestate information
				player_positions, player_scores = game_state
				player_positions = list(player_positions)
				player_scores = list(player_scores)

				p_i = self.current_player

				#update the current player positions
				player_positions[p_i] = (player_positions[p_i] + roll_value - 1) % 10 + 1

				#update playerer score
				player_scores[p_i] += player_positions[p_i]				

				#if there is a winner add this to the list of completed games
				if player_scores[p_i] >= self.game_end_value:
					
					#winner, scores
					game_end_tuple = (p_i, tuple(player_scores))

					#there may already be winning states with this winner and these scores
					if game_end_tuple not in self.completed_games:
						self.completed_games[game_end_tuple] = 0

					self.completed_games[game_end_tuple] += next_state_dimension_count

				#otherwise update the gamestete histogram
				else:

					next_state_tuple = (tuple(player_positions), tuple(player_scores))

					
					#there may be dupliacte game states from different states/rolls					
					if next_state_tuple not in next_game_states:
						next_game_states[next_state_tuple] = 0

					next_game_states[next_state_tuple] += next_state_dimension_count

		#update the current player
		self.current_player = (p_i + 1) % self.number_players

		#update the game states
		self.ongoing_games = next_game_states


	def games_over(self):
		return len(self.ongoing_games) == 0



class Dice():

	def __init__(self, size, deterministic=True, start=1):

		self.size = size
		self.total_rolls = 0
		
		self.deterministic = deterministic
		self.current = start #only matters in deterministic		


	def roll_die(self, number_rolls=1):

		self.total_rolls += number_rolls

		prev_total_rolls = {0:1}
		for _ in range(number_rolls):

			next_values = self._do_roll()
			next_total_rolls = {}

			for nv in next_values:
				for pt in prev_total_rolls:
					
					value_count = next_values[nv]
					prev_total_count = prev_total_rolls[pt]
					next_count = value_count * prev_total_count

					#new value
					value = nv + pt

					if value not in next_total_rolls:
						next_total_rolls[value] = 0
					
					next_total_rolls[value] += next_count	

			prev_total_rolls = next_total_rolls				

		return prev_total_rolls


	#this should be a strategy pattern if there are more than 1 type of die in part2 but w/e
	def _do_roll(self):

		if self.deterministic:

			values = {self.current:1}

			self.current += 1

			if self.current > self.size:
				self.current = 1

		#quantum
		else:
			values = {n+1:1 for n in range(self.size)}

		return values


def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		starting_positions = []
		for input_line in input_stream:
			_, _, _, _, pos = input_line.strip().split(' ')
			starting_positions.append(int(pos))

	return starting_positions


def play_till_winner(game, turns=None):

	count = 0
	while (not game.games_over()) and ((turns is None) or (count < turns)):
		game.do_turn()		
		count+=1


def part1_score(game):

	only_game_state = list(game.completed_games.keys())[0]
	return game.die.total_rolls*min(only_game_state[1])


def part2_score(game):

	total_wins = [0 for _ in range(game.number_players)]

	for game_state in game.completed_games:

		winner_id, _ = game_state
		total_wins[winner_id] += game.completed_games[game_state]

	return max(total_wins)


start_time = time.time()


fname = "input21.txt"
#fname = "test21.txt"
starting_positions = load_stuff(fname)


game = DiracDiceGame(starting_positions, Dice(100), 1000)
play_till_winner(game)

p1answer = part1_score(game)
print(p1answer)


game = DiracDiceGame(starting_positions, Dice(3, deterministic=False), 21)
play_till_winner(game)

p2answer = part2_score(game)
print(p2answer)


end_time = time.time()
print(round(end_time-start_time, 4))
