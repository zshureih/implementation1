import sys
from collections import deque
from queue import PriorityQueue
import math

class riverBank:
    def __init__(self, chickens, wolves, boat):
        self.chickens = chickens #number of chickens on bank
        self.wolves = wolves #number of wolves on bank
        self.boat = boat #boolean flag for if boat is on bank
    
    # if returns 0, bank is unbalanced, player loses
    def checkBalance(self):
        if self.chickens >= self.wolves or self.chickens == 0:
            return 1
        else:
            return 0

class Game:
    def __init__(self, goalState, initalState):
        self.leftBank = riverBank(initalState[0][0], initalState[0][1], initalState[0][2])
        self.rightBank = riverBank(initalState[1][0], initalState[1][1], initalState[1][2])
        self.initState = initalState
        self.goalState = goalState # 2d array, first row is left bank, second row is right bank
        self.lastState = initalState
        self.expanded = 0 #number of expanded nodes so far
        self.totalChickens = initalState[0][0] + initalState[1][0]
        self.totalWolves = initalState[0][1] + initalState[1][1]

    def checkLoss(self):
        # if both banks are still in balance, player has not lost
        if self.leftBank.checkBalance() and self.rightBank.checkBalance():
            return 0
        else:
            return 1

    # if current state is goal state
    def checkWin(self):
        currentState = self.getCurrentState()

        if currentState[0][0] != self.goalState[0][0]:
            return 0
        if currentState[0][1] != self.goalState[0][1]:
            return 0
        if currentState[0][2] != self.goalState[0][2]:
            return 0
        if currentState[1][0] != self.goalState[1][0]:
            return 0
        if currentState[1][1] != self.goalState[1][1]:
            return 0
        if currentState[1][1] != self.goalState[1][1]:
            return 0

        return 1

    def getCurrentState(self):
        return [[self.leftBank.chickens, self.leftBank.wolves, self.leftBank.boat],
                [self.rightBank.chickens, self.rightBank.wolves, self.rightBank.boat]]

    def setCurrentState(self, state):
        self.lastState = self.getCurrentState()

        self.leftBank.chickens = state[0][0]
        self.leftBank.wolves = state[0][1]
        self.leftBank.boat = state[0][2]
        
        self.rightBank.chickens = state[1][0]
        self.rightBank.wolves = state[1][1]
        self.rightBank.boat = state[1][2]

    def oneChickenAction(self, startBank, destBank):
        # save current state for undo
        self.lastState = self.getCurrentState()

        destBank.chickens += 1
        startBank.chickens -= 1
        
        startBank.boat = 0
        destBank.boat = 1

        return self.getCurrentState()

    def twoChickenAction(self, startBank, destBank):
        # save current state for undo
        self.lastState = self.getCurrentState()

        destBank.chickens += 2
        startBank.chickens -= 2

        startBank.boat = 0
        destBank.boat = 1
        
        return self.getCurrentState()

    def oneWolfAction(self, startBank, destBank):
        # save current state for undo
        self.lastState = self.getCurrentState()

        destBank.wolves += 1
        startBank.wolves -= 1

        startBank.boat = 0
        destBank.boat = 1

        return self.getCurrentState()

    def twoWolfAction(self, startBank, destBank):
        # save current state for undo
        self.lastState = self.getCurrentState()

        destBank.wolves += 2
        startBank.wolves -= 2

        startBank.boat = 0
        destBank.boat = 1
   
        return self.getCurrentState()

    def oneEachAction(self, startBank, destBank):
        # save current state for undo
        self.lastState = self.getCurrentState()

        destBank.chickens += 1
        destBank.wolves += 1

        startBank.chickens -= 1
        startBank.wolves -= 1

        startBank.boat = 0
        destBank.boat = 1

        return self.getCurrentState()

    def undo(self):
        self.leftBank.chickens = self.lastState[0][0]
        self.leftBank.wolves = self.lastState[0][1]
        self.leftBank.boat = self.lastState[0][2]

        self.rightBank.chickens = self.lastState[1][0]
        self.rightBank.wolves = self.lastState[1][1]
        self.rightBank.boat = self.lastState[1][2]

    def possibleState(self):
        currentState = self.getCurrentState()

        # if number of units is greater than total defined at start, or less than zero
        if currentState[0][0] + currentState[1][0] > self.totalChickens or currentState[0][0] < 0 or currentState[1][0] < 0:
            return 0
        if currentState[0][1] + currentState[1][1] > self.totalWolves or currentState[0][1] < 0 or currentState[1][1] < 0:
            return 0
        if currentState[0][2] + currentState[1][2] > 1 or currentState[0][2] < 0 or currentState[1][2] < 0:
            return 0

        return 1 

    # expand the current state by attempting each general move
    # if the move results in a valid state (not losing and all units add up properly) add it to the frontier
    def getFrontier(self):
        frontier = []

        if self.leftBank.boat:
            successor = 0

            successor = self.oneChickenAction(self.leftBank, self.rightBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.twoChickenAction(self.leftBank, self.rightBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.oneWolfAction(self.leftBank, self.rightBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.oneEachAction(self.leftBank, self.rightBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.twoWolfAction(self.leftBank, self.rightBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

        else:
            successor = 0

            successor = self.oneChickenAction(self.rightBank, self.leftBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.twoChickenAction(self.rightBank, self.leftBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.oneWolfAction(self.rightBank, self.leftBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.oneEachAction(self.rightBank, self.leftBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.twoWolfAction(self.rightBank, self.leftBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()
                    
        return frontier

# get intial and goal files as [[X,X,X],[X,X,X]]
def parseInputs(initialStateFile, goalStateFile):
    initStateFile = open(initialStateFile)
    initState = []
    for i in range(2):
        initState.append([int(x) for x in next(initStateFile).split(',')])
    initStateFile.close()

    goalFile = open(goalStateFile)
    goalState = []
    for i in range(2):
        goalState.append([int(x) for x in next(goalFile).split(',')])
    goalFile.close()

    return initState, goalState

def bfsSolver(initialStateFile, goalStateFile):
    # initialize game
    initState, goalState = parseInputs(initialStateFile, goalStateFile)
    game = Game(goalState, initState)
    
    #initialize search problem
    explored = []
    parents = {}
    parents[0] = None
    frontier = deque([game.getCurrentState()])
    while(1):
        # if frontier is empty, we couldn't find goal
        if len(frontier) == 0:
            return False, False, game.expanded
        
        # dequeue from frontier
        current = frontier.popleft()
        game.setCurrentState(current)
        explored.append(current)

        # if current state is a win, return
        if game.checkWin():
            return explored, parents, game.expanded
        
        # expand current state
        game.expanded += 1
        successors = game.getFrontier()

        # add novel states to frontier
        for s in successors:
            if not s in frontier and not s in explored:
                frontier.append(s)
                parents[len(explored) + len(frontier) - 1] = game.getCurrentState()
    
def dfsSolver(initialStateFile, goalStateFile):
    # initialize game
    initState, goalState = parseInputs(initialStateFile, goalStateFile)
    game = Game(goalState, initState)

    #initialize search problem
    game = Game(goalState, initState)
    explored = [game.getCurrentState()]
    parents = {}
    parents[0] = None
    frontier = [game.getCurrentState()]

    while(1):
        if len(frontier) == 0:
                return False

        # get highest priority node in frontier
        child = frontier.pop()
        game.setCurrentState(child)

        # if node is goal state, terminate
        if game.checkWin():
            return explored, parents, game.expanded

        # expand frontier
        game.expanded += 1
        successors = game.getFrontier()

        # add novel states to frontier with priority f(n)
        for s in successors:
            if not s in frontier and not s in explored:
                frontier.append(s)
                explored.append(s)
                parents[len(parents)] = game.getCurrentState()

def iddfsSolver(initialStateFile, goalStateFile):
    # initialize game
    initState, goalState = parseInputs(initialStateFile, goalStateFile)

    maxDepth = 1000
    totalExpanded = 0

    # for iterating depths
    for d in range(maxDepth):
        # set up search problem
        game = Game(goalState, initState)
        explored = [game.getCurrentState()]
        parents = {}
        parents[0] = None
        frontier = [game.getCurrentState()]

        # run dfs keeping track of depth
        result = iddfsHelper(game, 0, d+1, explored, frontier, parents)

        # update total expanded nodes
        totalExpanded += game.expanded
        if result:
            return explored, parents, totalExpanded

    return False, False, totalExpanded

def iddfsHelper(game, depth, maxDepth, explored, frontier, parents):
    while (1):
        if depth >= maxDepth:
                return False

        # get highest priority node in frontier
        child = frontier.pop()
        game.setCurrentState(child)

        # if node is goal state, terminate
        if game.checkWin():
            return True

        # expand frontier
        game.expanded += 1
        successors = game.getFrontier()

        # add novel states to frontier with priority f(n)
        depth += 1
        for s in successors:
            if not s in frontier and not s in explored:
                frontier.append(s)
                explored.append(s)
                parents[len(parents)] = game.getCurrentState()

def aStarSolver(initialStateFile, goalStateFile):
    # init game
    initState, goalState = parseInputs(initialStateFile, goalStateFile)
    game = Game(goalState, initState)

    #initialize search problem
    explored = [game.getCurrentState()]
    parents = {}
    parents[0] = None
    pFrontier = PriorityQueue()
    frontier = [] #keep two frontiers so that I can actually see what is inside them

    # initialize frontiers
    pFrontier.put(game.getCurrentState(), 0)
    frontier.append(game.getCurrentState())

    while (1):
        # if frontier is empty, terminate
        if pFrontier.empty():
            return False, False, game.expanded
        
        # get highest priority node in frontier
        child = pFrontier.get()
        frontier.remove(child) #remove from trackable frontier
        game.setCurrentState(child)

        # if node is goal state, terminate
        if game.checkWin():
            return parents, explored, game.expanded

        # expand frontier
        game.expanded += 1
        successors = game.getFrontier()

        # add novel states to frontier with priority f(n)
        for s in successors:
            if not s in frontier and not s in explored:
                #calc f(n)
                h = aStarHn(game, s)
                g = aStarGn(game, s)
                f = h + g
                #add node
                pFrontier.put(s, f)
                frontier.append(s)
                explored.append(s)
                parents[len(parents)] = game.getCurrentState()

def aStarHn(game, nextState):
    # calc h(n)
    Hn = 0
    for i in range(len(game.goalState)):
        for j in range(len(game.goalState[0])):
            Hn += pow(nextState[i][j] - game.goalState[i][j], 2)

    return math.sqrt(Hn)

def aStarGn(game, nextState):
    currentState = game.getCurrentState()
    # calc g(n)
    Gn = 0
    for i in range(len(currentState)):
        for j in range(len(currentState[0])):
            Gn += pow(nextState[i][j] - currentState[i][j], 2)

    return math.sqrt(Gn)

def getPath(explored, parents):
    goalId = len(explored) - 1
    goalState = explored[goalId]
    finalPath = deque([goalId])
    while finalPath[0]:
        earliestNode = finalPath[0]
        parentState = parents[earliestNode]
        parentId = explored.index(parentState)
        finalPath.appendleft(parentId)

    return finalPath

def main():
    parents, explored, expanded = 0, 0, 0
    path = []
    if sys.argv[3] == "bfs":
        explored, parents, expanded = bfsSolver(sys.argv[1], sys.argv[2])
        path = getPath(explored, parents)

        if explored == False:
            print("number of expanded nodes", expanded)
            print("Could not find a solution")
        else:
            outFile = open(sys.argv[4], "w+")
            for s in path:
                print(explored[s])
                outFile.write(str(explored[s]) + "\n")
            outFile.close()
            print("number of expanded nodes", expanded)

    if sys.argv[3] == "dfs":
        explored, parents, expanded = dfsSolver(sys.argv[1], sys.argv[2])
        path = getPath(explored, parents)

        if explored == False:
            print("number of expanded nodes", expanded)
            print("Could not find a solution")
        else:
            outFile = open(sys.argv[4], "w+")
            for s in path:
                print(explored[s])
                outFile.write(str(explored[s]) + "\n")
            outFile.close()
            print("number of expanded nodes", expanded)

    if sys.argv[3] == "iddfs":
        explored, parents, expanded = iddfsSolver(sys.argv[1], sys.argv[2])
        path = getPath(explored, parents)

        if explored == False:
            print("number of expanded nodes", expanded)
            print("Could not find a solution")
        else:
            outFile = open(sys.argv[4], "w+")
            for s in path:
                print(explored[s])
                outFile.write(str(explored[s]) + "\n")
            outFile.close()
            print("number of expanded nodes", expanded)

    if sys.argv[3] == "astar":
        parents, explored, expanded = aStarSolver(sys.argv[1], sys.argv[2])

        path = getPath(explored, parents)

        if explored == False:
            print("number of expanded nodes", expanded)
            print("Could not find a solution")
        else:
            outFile = open(sys.argv[4], "w+")
            
            for s in path:
                print(explored[s])
                outFile.write(str(explored[s]) + "\n")
            outFile.close()
            print("number of expanded nodes", expanded)

if __name__ == "__main__":
    main()
