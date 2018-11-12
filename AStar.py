# const
GRID_SIZE = 20

# function responsible for write file "grid.txt"
def WriteGridFileToArray():
    gridArray = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    i = 0
    j = 0
    f = open('grid.txt', 'r')
    while True:
        ch=f.read(1)
        if not ch: break
        if ch != ' ':
            if ch != '\n':
                gridArray[j][i] = ch
                i = i + 1
            else:
                i = 0
                j = j+1
    return gridArray

# function search finish field in grid
# ASSUMPTION: the finish field value is 9
def FindFinishFieldInGrid(gridArray):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if gridArray[i][j] == "9":
                finishFieldCoordinates = [i, j]
                return finishFieldCoordinates

# function search first field in grid
# ASSUMPTION: the first field value is 1
def FindStartFieldInGrid(gridArray):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if gridArray[i][j] == "1":
                startFieldCoordinates = [i, j]
                return startFieldCoordinates

# function calculates the heuristic by the Euclidian method
def CalculateHeuristic_EuclidianMethod(last):
    # variables with finish field coordinates
    xValueOfFinishField = last[0]
    yValueOfFinishField = last[1]

    heuristicArray = [[9 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # fields calculate the lenght to finish field
            xToFinishField = xValueOfFinishField - i
            yToFinishField = yValueOfFinishField - j

            heuristics = abs(xToFinishField) + abs(yToFinishField)
            heuristicArray[i][j] = heuristics

    return heuristicArray

# function search parent for field with (x,y) coordinates
def CalculateParentForField(actualFieldXValue, actualFieldYValue, parentsArray):

    # parentArray has value describing the position of parent
    # 1 : parent is on top
    # 2 : parent is on right
    # 3 : parent is on bottom
    # 4 : parent is on left
    #
    # case is value from parentArray for field with (x,y) coordinates
    case = parentsArray[actualFieldXValue][actualFieldYValue]

    # array to return parent coordinates
    parentCoordinates = [0 for x in range(2)]

    if case == 1:
        # parent is on top
        parentCoordinates[0] = actualFieldXValue - 1
        parentCoordinates[1] = actualFieldYValue
    elif case == 2:
        # parent is on right
        parentCoordinates[0] = actualFieldXValue
        parentCoordinates[1] = actualFieldYValue + 1
    elif case == 3:
        # parent is on bottom
        parentCoordinates[0] = actualFieldXValue + 1
        parentCoordinates[1] = actualFieldYValue
    elif case == 4:
        # parent is on left
        parentCoordinates[0] = actualFieldXValue
        parentCoordinates[1] = actualFieldYValue - 1


    return parentCoordinates

# function calculate the G value for field
# with (x,y) coordinates and put this value to array with G values
# ARGUMENTS: function takes 'parentArray' in arguments because
# G = parent G + 1
# RETURN: G array with changes (with G value of Field)
def CalculateGValueForField(actualFieldXValue, actualFieldYValue, parentsArray, gValuesArray):
    theGValueOfParent = gValuesArray[parentsArray[0]][parentsArray[1]]
    gValuesArray[actualFieldXValue][actualFieldYValue] = theGValueOfParent + 1
    return gValuesArray

# function calculate the F value for field
# with (x,y) coordinates and put this value to array with F values
# ARGUMENTS: function takes 'F', 'G' and 'H' arrays because
# F value = G value + H value
# RETURN: F array with changes (with F value of Field)
def CalculateFValueForField(actualFieldXValue, actualFieldYValue, fValuesArray, gValuesArray, heuristicArray):
    theGValueOfField = gValuesArray[actualFieldXValue][actualFieldYValue]
    theHValueOfField = heuristicArray[actualFieldXValue][actualFieldYValue]
    theFValueOfField = theGValueOfField + theHValueOfField
    fValuesArray[actualFieldXValue][actualFieldYValue] = theFValueOfField
    return fValuesArray

# function search neighbors for the field
# with (x,y) coordinates
def SearchForNeighbors(actualFieldXValue, actualFieldYValue, gridArray, typeOfFieldArray):

    # arrays with X, Y and Parents values for all potential neighbors
    arrayWithXValuesOfPotentialNeighbors = [999 for x in range(4)]
    arrayWithYValuesOfPotentialNeighbors = [999 for x in range(4)]
    arrayWithParentValuesOfPotentialNeighbors = [999 for x in range(4)]

    # array with neighbors that meet the conditions below:
    # 1) neighbor is on the grid
    # 2) neighbor is not obstacle
    # 3) neighbor is not on close list
    arrayWithNeighborsThatMeetTheConditions = []

    #TOP NEIGHBOOR
    arrayWithXValuesOfPotentialNeighbors[0] = actualFieldXValue - 1
    arrayWithYValuesOfPotentialNeighbors[0] = actualFieldYValue
    arrayWithParentValuesOfPotentialNeighbors[0] = 3

    #BOTTOM NEIGHBOOR
    arrayWithXValuesOfPotentialNeighbors[1] = actualFieldXValue + 1
    arrayWithYValuesOfPotentialNeighbors[1] = actualFieldYValue
    arrayWithParentValuesOfPotentialNeighbors[1] = 1

    #LEFT NEIGHBOOR
    arrayWithXValuesOfPotentialNeighbors[2] = actualFieldXValue
    arrayWithYValuesOfPotentialNeighbors[2] = actualFieldYValue - 1
    arrayWithParentValuesOfPotentialNeighbors[2] = 2

    #RIGHT NEIGHBOOR
    arrayWithXValuesOfPotentialNeighbors[3] = actualFieldXValue
    arrayWithYValuesOfPotentialNeighbors[3] = actualFieldYValue + 1
    arrayWithParentValuesOfPotentialNeighbors[3] = 4

    for i in range(4):
        # CONDITION: X and Y values are positive
        if not arrayWithXValuesOfPotentialNeighbors[i] < 0:
            if not arrayWithYValuesOfPotentialNeighbors[i] < 0:
                # CONDITION: X and Y values are less than grid size
                if arrayWithXValuesOfPotentialNeighbors[i] < (GRID_SIZE - 1):
                    if arrayWithYValuesOfPotentialNeighbors[i] < (GRID_SIZE - 1):
                        # CONDITION: Neighbor is not obstacle
                        if not gridArray[arrayWithXValuesOfPotentialNeighbors[i]][arrayWithYValuesOfPotentialNeighbors[i]] == '5':
                            # CONDITION: Neighbor is not on close list
                            if not typeOfFieldArray[arrayWithXValuesOfPotentialNeighbors[i]][arrayWithYValuesOfPotentialNeighbors[i]] == 2:
                                arrayWithNeighborsThatMeetTheConditions\
                                    .append([arrayWithXValuesOfPotentialNeighbors[i],arrayWithYValuesOfPotentialNeighbors[i],arrayWithParentValuesOfPotentialNeighbors[i]])

    return arrayWithNeighborsThatMeetTheConditions

# function calculate path from finish field to start field
def CalucatePath(actualFieldXValue, actualFieldYValue, parentsArray):
    path = []

    # x,y values are assigned to temporary values because they will be changed
    tempX = actualFieldXValue
    tempY = actualFieldYValue

    while True:
        # add field to path
        path.append([tempX,tempY])
        parentDirection = parentsArray[tempX][tempY]
        parentWhoIsOnThePath = CalculateParentForField(tempX, tempY, parentsArray)
        tempX = parentWhoIsOnThePath[0]
        tempY = parentWhoIsOnThePath[1]

        # when parent direction has value 0 - break
        # only start field has value 0 for parent direction
        if parentDirection == 0: break

    return path

# main function of program
def AStar():

    # declarations of all necessary arrays and values
    gridArray = WriteGridFileToArray().copy()
    finishField = FindFinishFieldInGrid(gridArray)
    startField = FindStartFieldInGrid(gridArray)
    heuristicArray = CalculateHeuristic_EuclidianMethod(finishField)
    fValuesArray = [[999 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]
    gValuesArray = [[999 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    # possible types of field:
    # 1 - field on open list
    # 2 - field on close list
    # 5 - field is obstacle
    typeOfFieldArray = [[0 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    # parentsArray has values they describe parent direction for field
    # possible values:
    # 1 - parent is on top
    # 2 - parent is on right
    # 3 - parent is on bottom
    # 4 - parent is on left
    # 9 - parent not yet calculate
    # 0 - field dont have parent, because it's start field
    parentsArray = [[9 for x in range(GRID_SIZE)] for y in range(GRID_SIZE)]

    # G value of start field is 0
    # also start field doesnt have parent so parent direction is 0
    gValuesArray[startField[0]][startField[1]] = 0
    parentsArray[startField[0]][startField[1]] = 0

    openList = []

    # start field is first field to run
    xValueOfActualField = startField[0]
    yValueOfActualField = startField[1]

    while True:
        actualParent = [99 for x in range(2)]

        # If value of actual field is 9 then finish the loop and calculate path
        # 9 says that the actual field is also finish field
        if gridArray[xValueOfActualField][yValueOfActualField] == '9':
            # calculate path
            path = CalucatePath(xValueOfActualField, yValueOfActualField, parentsArray)
            print("Path is : \n" + str(path))
            break

        # add actual field to open list
        typeOfFieldArray[xValueOfActualField][yValueOfActualField] = 1

        # dont calculate parent for start field
        if not parentsArray[xValueOfActualField][yValueOfActualField] == 0:
            actualParent = CalculateParentForField(xValueOfActualField, yValueOfActualField, parentsArray)

        # dont calculate G values for start field - it should be 0
        if not actualParent[1] == 99:
            gValuesArray = CalculateGValueForField(xValueOfActualField, yValueOfActualField, CalculateParentForField(xValueOfActualField, yValueOfActualField, parentsArray), gValuesArray)

        # update F values array with the F value of actual field
        fValuesArray = CalculateFValueForField(xValueOfActualField, yValueOfActualField, fValuesArray, gValuesArray, heuristicArray)

        # add actual field to close list
        typeOfFieldArray[xValueOfActualField][yValueOfActualField] = 2

        # search for neighbors for actual field
        neighbors = SearchForNeighbors(xValueOfActualField, yValueOfActualField, gridArray, typeOfFieldArray)

        # for all neighbors do changes:
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            # CHANGE #1: add neighbor to open list
            typeOfFieldArray[neighbor[0]][neighbor[1]] = 1
            # CHANGE #2: add parent direction to parent array
            parentsArray[neighbor[0]][neighbor[1]] = neighbor[2]
            # CHANGE #3: update G value array with G value of neighbor
            gValuesArray = CalculateGValueForField(neighbor[0], neighbor[1], CalculateParentForField(neighbor[0], neighbor[1], parentsArray), gValuesArray)
            # CHANGE #4: update F value array with F value of neighbor
            fValuesArray = CalculateFValueForField(neighbor[0], neighbor[1], fValuesArray, gValuesArray, heuristicArray)

        openList.clear()

        # search the entire grid for fields from the open list
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                # if field is on open list (type is 1)
                if typeOfFieldArray[i][j] == 1:
                    # add field to open list
                    openList.append([i,j])

        bestFValue = 999

        # if open list is empty there is no way to finish field
        if len(openList) == 0:
            print("Path not exist")
            break


        # for each field in open list
        # search for field with least F value
        for i in range(len(openList)):
            item = openList[i]
            if fValuesArray[item[0]][item[1]] < bestFValue:
                # check that field is on grid
                if item[0] < (GRID_SIZE - 1):
                    if item[1] < (GRID_SIZE - 1):
                        # update best F value for condition above
                        bestFValue = fValuesArray[item[0]][item[1]]
                        # update actual field coordinates with coordinates field with least F value
                        xValueOfActualField = item[0]
                        yValueOfActualField = item[1]



# Run AStart function (main function)
AStar()