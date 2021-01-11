import copy

class Direction:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    @staticmethod
    def determine_direction(prev_ind, next_ind):
        
        direction = None
        if prev_ind[0] - 1 == next_ind[0]:
            direction = Direction.UP
        elif prev_ind[0] + 1 == next_ind[0]:
            direction = Direction.DOWN
        elif prev_ind[1] + 1 == next_ind[1]:
            direction = Direction.RIGHT
        elif prev_ind[1] - 1 == next_ind[1]:
            direction = Direction.LEFT
        else:
            assert True, "Unspecified direction"
        return direction

    @staticmethod
    def get_index_in_direction(index, direction):

        next_index = copy.deepcopy(index)
        if direction is Direction.LEFT:
            next_index[1] -= 1
        elif direction is Direction.RIGHT:
            next_index[1] += 1
        elif direction is Direction.UP:
            next_index[0] -= 1
        elif direction is Direction.DOWN:
            next_index[0] += 1
        else:
            assert True, "Wrong direction " + str(direction)
        return next_index


if __name__ == '__main__':
    import doctest
    doctest.testmod()
