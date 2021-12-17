import io


def load_stuff(fname, part=1):
	with io.open(fname, 'r', encoding='utf-8') as input_stream: 

		area_bounds = input_stream.readline().strip()[13:]
		area_bounds_x, area_bounds_y = area_bounds.split(',')
		
		x1,x2 = [int(p) for p in (area_bounds_x.strip()[2:]).split('..')]
		y1,y2 = [int(p) for p in (area_bounds_y.strip()[2:]).split('..')]
		
		return x1,x2,y1,y2


"""
up is the same as left or right

p1 <= p2

note that in gravity the path going up is the same as the path going down until you pass 0
"""
def find_all_good_velocity(p1,p2,gravity=False):

	"""
	if we are stradling 0 all values are good if they are values in the bounds and there is no gravity
	if there is gravity then a shot of v is good if a shot of -(v-1) is good and shots of [0,-v] are 
	
	"""
	
	if (p1 <= 0) and (p2 >= 0):

		return list(range(p1, p2+1 if not gravity else max([p2+1, -p1])))

	elif (p1 < 0) and (p2 < 0):
		r1, r2 = -p2, -p1

	elif (p1 > 0) and (p2 > 0):
		r1, r2 = p1, p2
		gravity = False #gravity never matters in this case even if it is on
		
	good_velocity = []
	#velocities over r2 can never hit the target space
	for velocity in range(0, r2+1):
		
		v = velocity
		position = v
		isGood = False

		#stop if we have gone past the zone
		while (position <= r2) and (not isGood) and ((v > 0) or gravity):
			
			#if we are in the zone 
			if (r1 <= position) and (position <= r2):
				isGood = True
				
			v += 1 if gravity else -1
			position += v

		if isGood:
			good_velocity.append(velocity)


	#if we were calculated falling (gravity only on if falling)
	if gravity:
		#good down speed of -v has corresponding speed (v-1)
		up_good_velocity = [v-1 for v in good_velocity] #what about -1? 0 only in list if 1 is

		#need to flip the other velocities to negative 
		good_velocity = [-v for v in good_velocity] + up_good_velocity


	return sorted(list(set(good_velocity)))


#non-negative y velocities always exist
def max_y_position(good_velocity_y):

	best_pos = max(good_velocity_y)

	return (best_pos+1)*best_pos//2


def good_velocity_pairs(x1,x2,y1,y2,velocity_x,velocity_y):

	good_velocity_pairs_count = 0
	stop_condition = min([-abs(y1), -abs(y2)])

	for start_vx in velocity_x:
		for start_vy in velocity_y:	
			
			vx,vy =	start_vx,start_vy			
			px,py = 0,0
			keep_checking = True

			while(keep_checking):

				#print(vx,vy, px, py)
				#if we are in the box count it and move on
				if (x1 <= px) and (px <= x2) and (y1 <= py) and (py <= y2):
					good_velocity_pairs_count += 1
					keep_checking = False

				else:
					px += vx
					py += vy

					#vx tends towards 0
					vx -= 1 if vx > 0 else -1 if vx < 0 else 0
					#vy always down
					vy -= 1					

					"""
					could do complex end condition but also can just make sure py >= min(-abs(y1), -abs(y2))
					as this will always happen from gravity and if it does we can never get in the square
					"""
					keep_checking = py >= stop_condition

	return good_velocity_pairs_count


"""
idea, find all good 1D velocities
count the ones that match in 2D
"""
fname = "input17.txt"
x1,x2,y1,y2 = load_stuff(fname)
good_velocity_x = find_all_good_velocity(x1,x2,gravity=False)
good_velocity_y = find_all_good_velocity(y1,y2,gravity=True)
best_y_pos = max_y_position(good_velocity_y)
print(best_y_pos)
good_velocity_pairs_count = good_velocity_pairs(x1,x2,y1,y2,good_velocity_x, good_velocity_y)
print(good_velocity_pairs_count)
