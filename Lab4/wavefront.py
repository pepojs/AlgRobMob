import numpy as np
import logging
import copy
import matplotlib.pyplot as plt

from direction import Direction


def is_robot(cell):
	return True if cell == -np.inf else False


def wavefront_map(mapa, goal, robot, level):
	arr = np.full(mapa.shape, np.nan, dtype=float)

	for i in range(mapa.shape[0]):
		for j in range(mapa.shape[1]):
			if mapa[i][j] > level:
				arr[i][j] = np.inf


	arr[goal[1]][goal[0]] = 0
	arr[robot[1]][robot[0]] = -np.inf
	curr_max_value = 0
	
	is_finished = False
	while not is_finished:
		max_indices = np.argwhere(arr == curr_max_value)
		for index in max_indices:
			next_indices = [
				[index[0] - 1, index[1]],
				[index[0] + 1, index[1]],
				[index[0], index[1] - 1],
				[index[0], index[1] + 1],
			]
			
			counter = 0
			for i in next_indices:
				if arr[i[0]][i[1]] == np.inf:
					counter += 1

			if counter == len(next_indices):
				print('Not posible moves')	
				return arr
		
			for next_index in next_indices:
				if next_index[0] in range(arr.shape[0]) and next_index[1] in range(arr.shape[1]):
					if arr[next_index[0]][next_index[1]] != np.inf:
						
						if arr[next_index[0]][next_index[1]] == -np.inf:
							is_finished = True
							print("Start position has been found!")
							arr[next_index[0]][next_index[1]] = curr_max_value + 1
							break
						elif np.isnan(arr[next_index[0]][next_index[1]]):
							is_finished = False
							arr[next_index[0]][next_index[1]] = curr_max_value + 1
			if is_finished:
				break
		curr_max_value += 1

	return arr
#print("Map: \n" + str(arr))
#print("Current maximum value: " + str(curr_max_value))


# Finding the shortest path preserving minimal number of turns
def path_planning(arr,robot):
	moves = [
		Direction.DOWN,
		Direction.UP,
		Direction.LEFT,
		Direction.RIGHT,
	]

	current_field_value = arr[robot[1]][robot[0]]
	current_field_index = [robot[1], robot[0]]
	path = [current_field_index]
	movesList = []
	last_direction = None

	while current_field_value != 0:
		if last_direction:
			field_index = Direction.get_index_in_direction(current_field_index, last_direction)
			field_value = arr[field_index[0]][field_index[1]]
			if field_value < current_field_value:
				current_field_index = field_index
				current_field_value = field_value
				path.append(field_index)
				movesList.append(last_direction)
				continue
		for move in moves:
			field_index = Direction.get_index_in_direction(current_field_index, move)
			if arr[field_index[0]][field_index[1]] < current_field_value:
				current_field_value = arr[field_index[0]][field_index[1]]
				current_field_index = field_index
				path.append(field_index)
				last_direction = move
				movesList.append(last_direction)
				break
	return path, movesList
				

#logging.info('Determined path: \n' + str(path))
