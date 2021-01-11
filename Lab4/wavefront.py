import numpy as np
import logging
import copy

from direction import Direction


def is_robot(cell):
    return True if cell == -np.inf else False


arr = np.full((8, 7), np.nan, dtype=float)
obs = [(1, 1), (1, 2), (1, 4), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (5, 1),
       (4, 1), (3, 1), (2, 1)]
goal = (5, 2)
robot = (2, 4)

for o in obs:
    arr[o[0]][o[1]] = np.inf

arr[goal[0]][goal[1]] = 0
arr[robot[0]][robot[1]] = -np.inf
curr_max_value = 0
logging.debug(str(np.argwhere(arr == curr_max_value)))

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

print("Map: \n" + str(arr))
print("Current maximum value: " + str(curr_max_value))


# Finding the shortest path preserving minimal number of turns

moves = [
    Direction.DOWN,
    Direction.UP,
    Direction.LEFT,
    Direction.RIGHT,
]

current_field_value = arr[robot[0]][robot[1]]
current_field_index = [robot[0], robot[1]]
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

print('Determined path: \n' + str(path))
print('Moves list: {}'.format(movesList))
