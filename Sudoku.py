#
# "HELLO WORLD!" EVOLUTIONARY ALGORITHM  
#

import random
import os
### EVOLUTIONARY ALGORITHM ###

def evolve():
    population = create_pop()
    fitness_population = evaluate_pop(population)
    best_ind, best_fit = best_pop(population, fitness_population)
    gen = 0
    bestgen = 0 
    CurrentBest = 54
    AllTimeBest_ind = [best_ind.copy()]
    AllTimeBest_fit = best_fit
    while best_fit != 0 and gen != NUMBER_GENERATION:
        gen +=1
        bestgen +=1
        #this if statement is for when the results stagnate
        if bestgen > MAX_REPEATS:
            bestgen = 0
            population = create_pop()
            #I found that the populations under 100 needed help from previous runs in order to make improvements on fitness score, the 1000 and 10000 were fine though
            if POPULATION_SIZE <= 100:
                population[0] = random.choice(AllTimeBest_ind)
            fitness_population = evaluate_pop(population)
            best_ind, best_fit = best_pop(population, fitness_population)
            CurrentBest = 54
            print("Restart Due To Local Minimum")
 
        
        mating_pool = select_pop(population, fitness_population)
        offspring_population = crossover_pop(mating_pool)
        population = mutate_pop(offspring_population)
        fitness_population = evaluate_pop(population)
        best_ind, best_fit = best_pop(population, fitness_population)
        if CurrentBest > best_fit:
            bestgen = 0
            CurrentBest = best_fit
        if best_fit < AllTimeBest_fit:
            AllTimeBest_ind = [best_ind.copy()]
            AllTimeBest_fit = best_fit
        elif best_fit == AllTimeBest_fit:
            AllTimeBest_ind.append(best_ind)



            
        print( "#%3d" % gen, "fit:%3d" % best_fit, "".join(best_ind))

### POPULATION-LEVEL OPERATORS ###

def create_pop():
    return [ create_ind() for _ in range(POPULATION_SIZE) ]

def evaluate_pop(population):
    return [ evaluate_ind(individual) for individual in population ]

def select_pop(population, fitness_population):
    sorted_population = sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])
    return [ individual for individual, fitness in sorted_population[:int(POPULATION_SIZE * TRUNCATION_RATE)] ]


def crossover_pop(population):
    return [ crossover_ind(random.choice(population), random.choice(population)) for _ in range(POPULATION_SIZE) ]

def mutate_pop(population):
    return [ mutate_ind(individual) for individual in population ]

def best_pop(population, fitness_population):
    return sorted(zip(population, fitness_population), key = lambda ind_fit: ind_fit[1])[0]

def spike_pop(population):
    return[repeatRandomizeSubgrid(individual) for individual in population]

### INDIVIDUAL-LEVEL OPERATORS: REPRESENTATION & PROBLEM SPECIFIC ###

target  = list("HELLO WORLD!")
alphabet = " !ABCDEFGHIJLKLMNOPQRSTUVWXYZ"
INDIVIDUAL_SIZE = len(target)

def create_ind():
    return CreateSudoku(RandomFill(EMPTY_SUDOKU, CONSTANTS),CONSTANTS)

def evaluate_ind(individual):
    return evaluateSudoku(individual)

def crossover_ind(individual1, individual2):
    return( [ random.choice(ch_pair) for ch_pair in zip(individual1, individual2) ])

def mutate_ind(individual):
    """
    Summary line.

    This takes an individual and returns the mutated individual by spliting it into subgrids.

    Parameters
    ----------
    arg1 : List
        Sudoku
    
    Returns 
    -------
    List
        a mutated sudoku as a list

    """
    indexes = SquareCheckIndex
    mutateList = []
    for i in range(len(indexes)):
        tempList = []
        currentrowindex = indexes[i]
        for j in currentrowindex:
            tempList.append(individual[j])
        mutateList.append(tempList)
    for k in range(len(mutateList)):
        mutateList[k] = MutateSubGrid(mutateList[k], k)

    for x in range(len(indexes)):
        for y in range(len(indexes)):
            index = indexes[x][y]
            individual[index] = mutateList[x][y]                 
    return individual
def randomize_ind_subGrid(individual):
    return(random)

############     ####################

def Read_Text_File(Filename):
    """
    Summary line.

    This reads the File and returns the sudoku as a string

    Parameters
    ----------
    arg1 : File
        Path to the File
    
    Returns 
    -------
    String
        sudoku as a string with 0 in empty squares.

    """
    
    f = open(Filename, "r")
    llist = []
    for x in f:
        x = x[:-1]
        x = x.replace(".", "0")
        x = x.replace("!", "")
        if "-" not in x:
            llist.append(x)

    
    Sudoku_String = ''.join(llist)
    return Sudoku_String


def Constants(SString):
    """
    Summary line.

    This returns the Indexes that must remain the same

    Parameters
    ----------
    arg1 : String
        Sudoku with 0 in empty spaces
    
    Returns 
    -------
    List
        List of indexes that shouldnt change

    """
    
    IndexList = []
    for i in range(len(SString)):
        if SString[i] != "0":
            IndexList.append(i)
    return IndexList


def RandomFill(SString, IndexList):
    """
    Summary line.

    This fills the sudoku with random numbers from 1 to 9 

    Parameters
    ----------
    arg1 : String
        Sudoku as a String
    
    arg2 : List
        List of indexes that must not change
    
    Returns 
    -------
    List
        a sudoku as a list with values filled in

    """
    F= list(SString)
    for j in range(len(F)):
        if F[j] == "0" and (j not in IndexList):
            number = str(random.randint(1,9))
            F[j] = number
    return F


def Setup(List, indexes, Constants=[]):
    """
    Summary line.

    This removes the duplicates from the subgrids

    Parameters
    ----------
    arg1 : List
        Sudoku as a list of values
    
    arg2 : List
        List of indexes that are to be changed
    
    arg3 : List
        List of indexes that must not change
    
    Returns 
    -------
    List
        list of 9 unique values

    """
    Vals = ['1','2','3','4','5','6','7','8','9']
    Visited = []
    for i in range(len(indexes)):
        if indexes[i] in Constants:
            Visited.append(List[i])
            Vals.remove(List[i])

    ChangeIndex = []
    for i in range(len(List)):
        if List[i] not in Visited:
            Vals.remove(List[i])
            Visited.append(List[i])
        elif(indexes[i] not in Constants):
            ChangeIndex.append(i)
    for x in ChangeIndex:
        y = random.choice(Vals)
        List[x] = y
        Vals.remove(y)
    return List

def CreateSudoku(sudoku, Constants):
    """
    Summary line.

    This creates a sudoku by using setup and the sudoku string with duplicates in it

    Parameters
    ----------
    arg1 : List
        Sudoku as a list of values
    
    arg2 : List
        List of indexes that are to be changed
    
    Returns 
    -------
    List
        a Sudoku filled in as a list 

    """
    
    indexes = SquareCheckIndex
    mutateList = []
    for i in range(len(indexes)):
        tempList = []
        currentrowindex = indexes[i]
        for j in currentrowindex:
            tempList.append(sudoku[j])
        mutateList.append(tempList)
    for k in range(len(mutateList)):
        mutateList[k] = Setup(mutateList[k], indexes[k], Constants)
    
    for x in range(len(indexes)):
        for y in range(len(indexes)):
            index = indexes[x][y]
            sudoku[index] = mutateList[x][y]
    return sudoku


def evaluateSudoku(sudoku):
    """
    Summary line.

    This returns a fitness based on the duplicates in the rows and 

    Parameters
    ----------
    arg1 : List
        Sudoku as a list of values
    
    
    Returns 
    -------
    int
        A fitness value for the sudoku

    """
    
    fitness = 0
    rowduplicates = 0
    columnduplicates = 0
    squareduplicates = 0
    for i in range(9):
        SquareIndexesToCheck = []
        RowIndexesToCheck = []
        ColumnIndexesToCheck = []
        for j in range(9):
            RowIndexesToCheck.append(sudoku[RowCheckIndex[i][j]])
            SquareIndexesToCheck.append(sudoku[SquareCheckIndex[i][j]])
            ColumnIndexesToCheck.append(sudoku[ColumnCheckIndex[i][j]])
        rowduplicates = 9-len(set(RowIndexesToCheck))
        columnduplicates = 9- len(set(ColumnIndexesToCheck))
        squareduplicates = 9- len(set(SquareIndexesToCheck))
        fitness = fitness + rowduplicates + columnduplicates + squareduplicates
    return fitness

def MutateSubGrid(SubGrid, SubGridNumber):
    
    """
    Summary line.

    Swaps numbers in subgrid randomly, doesnt swap the constant numbers from the origional grid

    Parameters
    ----------
    arg1 : List
        a sub grid of a Sudoku as a list of values
    
    arg2 : int
        the position of the subgrid in the sudoku
    
    Returns 
    -------
    list
        a mutated list from the sub grid

    """
    DontChange = []
    for i in range(len(SubGrid)):
        if SquareCheckIndex[SubGridNumber][i] in CONSTANTS:
            DontChange.append(SubGrid[i])

            
    for i in range(len(SubGrid)):
        if random.random()<MUTATION_RATE and SubGrid[i] not in DontChange:
            position_change = -999
            while position_change == -999 or SubGrid[position_change] in DontChange:
                position_change = random.randint(0,8)
            SubGrid[i], SubGrid[position_change] = SubGrid[position_change], SubGrid[i]
    return SubGrid


### PARAMERS VALUES ###k




grid = input("what grid? ")
path = os.getcwd()+ '\\grid'+str(grid)+'.ss.txt'
POPULATION_SIZE = int(input("Population Size?  "))
MAX_REPEATS = int(input("Maximum number of repeats before restart due to local minimum?  "))
MUTATION_RATE = float(input("what is the Mutation Rate between 0 and 1 ?"))
TRUNCATION_RATE = float(input("what is the Truncation Rate between 0 and 1 ?"))
NUMBER_GENERATION = 1000000000000
EMPTY_SUDOKU = Read_Text_File(path) 
CONSTANTS = Constants(EMPTY_SUDOKU)
SquareCheckIndex = [[0, 1, 2, 9, 10, 11, 18, 19, 20], [3, 4, 5, 12, 13, 14, 21, 22, 23], [6, 7, 8, 15, 16, 17, 24, 25, 26], [27, 28, 29, 36, 37, 38, 45, 46, 47], [30, 31, 32, 39, 40, 41, 48, 49, 50], [33, 34, 35, 42, 43, 44, 51, 52, 53], [54, 55, 56, 63, 64, 65, 72, 73, 74], [57, 58, 59, 66, 67, 68, 75, 76, 77], [60, 61, 62, 69, 70, 71, 78, 79, 80]]
RowCheckIndex = [[0, 1, 2, 3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15, 16, 17], [18, 19, 20, 21, 22, 23, 24, 25, 26], [27, 28, 29, 30, 31, 32, 33, 34, 35], [36, 37, 38, 39, 40, 41, 42, 43, 44], [45, 46, 47, 48, 49, 50, 51, 52, 53], [54, 55, 56, 57, 58, 59, 60, 61, 62], [63, 64, 65, 66, 67, 68, 69, 70, 71], [72, 73, 74, 75, 76, 77, 78, 79, 80]]
ColumnCheckIndex = [[0, 9, 18, 27, 36, 45, 54, 63, 72], [1, 10, 19, 28, 37, 46, 55, 64, 73], [2, 11, 20, 29, 38, 47, 56, 65, 74], [3, 12, 21, 30, 39, 48, 57, 66, 75], [4, 13, 22, 31, 40, 49, 58, 67, 76], [5, 14, 23, 32, 41, 50, 59, 68, 77], [6, 15, 24, 33, 42, 51, 60, 69, 78], [7, 16, 25, 34, 43, 52, 61, 70, 79], [8, 17, 26, 35, 44, 53, 62, 71, 80]]
### EVOLVE! ###


evolve()
