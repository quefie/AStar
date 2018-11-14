# const
GRID_SIZE = 20


# function responsible for write file "grid.txt"
def write_grid_file_to_array():
    grid_array = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    i = 0
    j = 0
    file = open('grid.txt', 'r')
    while True:
        char = file.read(1)
        if not char:
            break
        if char != ' ':
            if char != '\n':
                grid_array[j][i] = char
                i = i + 1
            else:
                i = 0
                j = j + 1
    return grid_array


# function search finish field in grid
# ASSUMPTION: the finish field value is 9
def find_finish_field_in_grid(grid_array):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid_array[i][j] == "9":
                finish_field_coordinates = [i, j]
                return finish_field_coordinates


# function search first field in grid
# ASSUMPTION: the first field value is 1
def find_start_field_in_grid(grid_array):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid_array[i][j] == "1":
                start_field_coordinates = [i, j]
                return start_field_coordinates


# function calculates the heuristic by the Euclidian method
def calculate_heuristic_euclidian_method(last):
    # variables with finish field coordinates
    x_value_of_finish_field = last[0]
    y_value_of_finish_field = last[1]

    heuristic_array = [[9 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # fields calculate the lenght to finish field
            x_to_finish_field = x_value_of_finish_field - i
            y_to_finish_field = y_value_of_finish_field - j

            heuristics = abs(x_to_finish_field) + abs(y_to_finish_field)
            heuristic_array[i][j] = heuristics

    return heuristic_array


# function search parent for field with (x,y) coordinates
def calculate_parent_for_field(actual_field_x_value, actual_field_y_value, parents_array):
    # parentArray has value describing the position of parent
    # 1 : parent is on top
    # 2 : parent is on right
    # 3 : parent is on bottom
    # 4 : parent is on left
    #
    # case is value from parentArray for field with (x,y) coordinates
    case = parents_array[actual_field_x_value][actual_field_y_value]

    # array to return parent coordinates
    parent_coordinates = [0 for x in range(2)]

    if case == 1:
        # parent is on top
        parent_coordinates[0] = actual_field_x_value - 1
        parent_coordinates[1] = actual_field_y_value
    elif case == 2:
        # parent is on right
        parent_coordinates[0] = actual_field_x_value
        parent_coordinates[1] = actual_field_y_value + 1
    elif case == 3:
        # parent is on bottom
        parent_coordinates[0] = actual_field_x_value + 1
        parent_coordinates[1] = actual_field_y_value
    elif case == 4:
        # parent is on left
        parent_coordinates[0] = actual_field_x_value
        parent_coordinates[1] = actual_field_y_value - 1

    return parent_coordinates


# function calculate the G value for field
# with (x,y) coordinates and put this value to array with G values
# ARGUMENTS: function takes 'parentArray' in arguments because
# G = parent G + 1
# RETURN: G array with changes (with G value of Field)
def calculate_g_value_for_field(actual_field_x_value, actual_field_y_value, parents_array, g_values_array):
    the_g_value_of_parent = g_values_array[parents_array[0]][parents_array[1]]
    g_values_array[actual_field_x_value][actual_field_y_value] = the_g_value_of_parent + 1
    return g_values_array


# function calculate the F value for field
# with (x,y) coordinates and put this value to array with F values
# ARGUMENTS: function takes 'F', 'G' and 'H' arrays because
# F value = G value + H value
# RETURN: F array with changes (with F value of Field)
def calculate_f_value_for_field(actual_field_x_value, actual_field_y_value, f_values_array, g_values_array, heuristic_array):
    the_g_value_of_field = g_values_array[actual_field_x_value][actual_field_y_value]
    the_h_value_of_field = heuristic_array[actual_field_x_value][actual_field_y_value]
    the_f_value_of_field = the_g_value_of_field + the_h_value_of_field
    f_values_array[actual_field_x_value][actual_field_y_value] = the_f_value_of_field
    return f_values_array


# function search neighbors for the field
# with (x,y) coordinates
def search_for_neighbors(actual_field_x_value, actual_field_y_value, grid_array, type_of_field_array):
    # arrays with X, Y and Parents values for all potential neighbors
    array_with_x_values_of_potential_neighbors = [999 for x in range(4)]
    array_with_y_values_of_potential_neighbors = [999 for x in range(4)]
    array_with_parent_values_of_potential_neighbors = [999 for x in range(4)]

    # array with neighbors that meet the conditions below:
    # 1) neighbor is on the grid
    # 2) neighbor is not obstacle
    # 3) neighbor is not on close list
    array_with_neighbors_that_meet_the_conditions = []

    # TOP NEIGHBOOR
    array_with_x_values_of_potential_neighbors[0] = actual_field_x_value - 1
    array_with_y_values_of_potential_neighbors[0] = actual_field_y_value
    array_with_parent_values_of_potential_neighbors[0] = 3

    # BOTTOM NEIGHBOOR
    array_with_x_values_of_potential_neighbors[1] = actual_field_x_value + 1
    array_with_y_values_of_potential_neighbors[1] = actual_field_y_value
    array_with_parent_values_of_potential_neighbors[1] = 1

    # LEFT NEIGHBOOR
    array_with_x_values_of_potential_neighbors[2] = actual_field_x_value
    array_with_y_values_of_potential_neighbors[2] = actual_field_y_value - 1
    array_with_parent_values_of_potential_neighbors[2] = 2

    # RIGHT NEIGHBOOR
    array_with_x_values_of_potential_neighbors[3] = actual_field_x_value
    array_with_y_values_of_potential_neighbors[3] = actual_field_y_value + 1
    array_with_parent_values_of_potential_neighbors[3] = 4

    for i in range(4):
        # CONDITION: X and Y values are positive
        if not array_with_x_values_of_potential_neighbors[i] < 0:
            if not array_with_y_values_of_potential_neighbors[i] < 0:
                # CONDITION: X and Y values are less than grid size
                if array_with_x_values_of_potential_neighbors[i] < (GRID_SIZE - 1):
                    if array_with_y_values_of_potential_neighbors[i] < (GRID_SIZE - 1):
                        # CONDITION: Neighbor is not obstacle
                        if not grid_array[array_with_x_values_of_potential_neighbors[i]][
                                   array_with_y_values_of_potential_neighbors[i]] == '5':
                            # CONDITION: Neighbor is not on close list
                            if not type_of_field_array[array_with_x_values_of_potential_neighbors[i]][
                                       array_with_y_values_of_potential_neighbors[i]] == 2:
                                array_with_neighbors_that_meet_the_conditions \
                                    .append([array_with_x_values_of_potential_neighbors[i],
                                             array_with_y_values_of_potential_neighbors[i],
                                             array_with_parent_values_of_potential_neighbors[i]])

    return array_with_neighbors_that_meet_the_conditions


# function calculate path from finish field to start field
def calucate_path(actual_field_x_value, actual_field_y_value, parents_array):
    path = []

    # x,y values are assigned to temporary values because they will be changed
    temp_x = actual_field_x_value
    temp_y = actual_field_y_value

    while True:
        # add field to path
        path.append([temp_x, temp_y])
        parent_direction = parents_array[temp_x][temp_y]
        parent_who_is_on_the_path = calculate_parent_for_field(temp_x, temp_y, parents_array)
        temp_x = parent_who_is_on_the_path[0]
        temp_y = parent_who_is_on_the_path[1]

        # when parent direction has value 0 - break
        # only start field has value 0 for parent direction
        if parent_direction == 0:
            break

    return path


# main function of program
def a_star():
    # declarations of all necessary arrays and values
    grid_array = write_grid_file_to_array().copy()
    finish_field = find_finish_field_in_grid(grid_array)
    start_field = find_start_field_in_grid(grid_array)
    heuristic_array = calculate_heuristic_euclidian_method(finish_field)
    f_values_array = [[999 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    g_values_array = [[999 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    # possible types of field:
    # 1 - field on open list
    # 2 - field on close list
    # 5 - field is obstacle
    type_of_field_array = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    # parentsArray has values they describe parent direction for field
    # possible values:
    # 1 - parent is on top
    # 2 - parent is on right
    # 3 - parent is on bottom
    # 4 - parent is on left
    # 9 - parent not yet calculate
    # 0 - field dont have parent, because it's start field
    parents_array = [[9 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    # G value of start field is 0
    # also start field doesnt have parent so parent direction is 0
    g_values_array[start_field[0]][start_field[1]] = 0
    parents_array[start_field[0]][start_field[1]] = 0

    open_list = []

    # start field is first field to run
    x_value_of_actual_field = start_field[0]
    y_value_of_actual_field = start_field[1]

    while True:
        actual_parent = [99 for x in range(2)]

        # If value of actual field is 9 then finish the loop and calculate path
        # 9 says that the actual field is also finish field
        if grid_array[x_value_of_actual_field][y_value_of_actual_field] == '9':
            # calculate path
            path = calucate_path(x_value_of_actual_field, y_value_of_actual_field, parents_array)
            print("Path is : \n" + str(path))
            break

        # add actual field to open list
        type_of_field_array[x_value_of_actual_field][y_value_of_actual_field] = 1

        # dont calculate parent for start field
        if not parents_array[x_value_of_actual_field][y_value_of_actual_field] == 0:
            actual_parent = calculate_parent_for_field(x_value_of_actual_field, y_value_of_actual_field, parents_array)

        # dont calculate G values for start field - it should be 0
        if not actual_parent[1] == 99:
            g_values_array = calculate_g_value_for_field(x_value_of_actual_field, y_value_of_actual_field,
                                                         calculate_parent_for_field(x_value_of_actual_field,
                                                                                    y_value_of_actual_field,
                                                                                    parents_array), g_values_array)

        # update F values array with the F value of actual field
        f_values_array = calculate_f_value_for_field(x_value_of_actual_field, y_value_of_actual_field, f_values_array,
                                                     g_values_array, heuristic_array)

        # add actual field to close list
        type_of_field_array[x_value_of_actual_field][y_value_of_actual_field] = 2

        # search for neighbors for actual field
        neighbors = search_for_neighbors(x_value_of_actual_field, y_value_of_actual_field, grid_array, type_of_field_array)

        # for all neighbors do changes:
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            # CHANGE #1: add neighbor to open list
            type_of_field_array[neighbor[0]][neighbor[1]] = 1
            # CHANGE #2: add parent direction to parent array
            parents_array[neighbor[0]][neighbor[1]] = neighbor[2]
            # CHANGE #3: update G value array with G value of neighbor
            g_values_array = calculate_g_value_for_field(neighbor[0], neighbor[1],
                                                         calculate_parent_for_field(neighbor[0], neighbor[1],
                                                                                    parents_array), g_values_array)
            # CHANGE #4: update F value array with F value of neighbor
            f_values_array = calculate_f_value_for_field(neighbor[0], neighbor[1], f_values_array, g_values_array,
                                                         heuristic_array)

        open_list.clear()

        # search the entire grid for fields from the open list
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # if field is on open list (type is 1)
                if type_of_field_array[i][j] == 1:
                    # add field to open list
                    open_list.append([i, j])

        best_f_value = 999

        # if open list is empty there is no way to finish field
        if len(open_list) == 0:
            print("Path not exist")
            break

        # for each field in open list
        # search for field with least F value
        for i in range(len(open_list)):
            item = open_list[i]
            if f_values_array[item[0]][item[1]] < best_f_value:
                # check that field is on grid
                if item[0] < (GRID_SIZE - 1):
                    if item[1] < (GRID_SIZE - 1):
                        # update best F value for condition above
                        best_f_value = f_values_array[item[0]][item[1]]
                        # update actual field coordinates with coordinates field with least F value
                        x_value_of_actual_field = item[0]
                        y_value_of_actual_field = item[1]


# Run AStart function (main function)
a_star()
