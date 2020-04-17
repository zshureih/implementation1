import sys

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
        self.goalState = goalState # 2d array, first row is left bank, second row is right bank
        self.lastState = initalState

    def checkLoss(self):
        # if both banks are still in balance, player has not lost
        if self.leftBank.checkBalance() and self.rightBank.checkBalance():
            return 
        else:
            return 1

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

        if currentState[0][0] + currentState[1][0] > 3 or currentState[0][0] < 0 or currentState[1][0] < 0:
            return 0
        if currentState[0][1] + currentState[1][1] > 3 or currentState[0][1] < 0 or currentState[1][1] < 0:
            return 0
        if currentState[0][2] + currentState[1][2] > 1 or currentState[0][2] < 0 or currentState[1][2] < 0:
            return 0

        return 1 

    def getFrontier(self):
        frontier = []
        # print(self.getCurrentState())
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

            successor = self.twoWolfAction(self.leftBank, self.rightBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.oneEachAction(self.leftBank, self.rightBank)
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

            successor = self.twoWolfAction(self.rightBank, self.leftBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()

            successor = self.oneEachAction(self.rightBank, self.leftBank)
            if not self.checkLoss() and self.possibleState():
                frontier.append(successor)
            self.undo()
        
        # print(frontier)
        return frontier

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

def bfsSolver(initialStateFile, goalStateFile, outputFile):
    # initialize game
    initState, goalState = parseInputs(initialStateFile, goalStateFile)

    game = Game(goalState, initState)
    #initialize search problem
    explored = []
    frontier = game.getFrontier()
    while(1):
        if len(frontier) == 0:
            return game.getCurrentState()
        
        child = frontier.pop()
        # print(frontier)
        # print(child)
        game.setCurrentState(child)
        # print(game.getCurrentState())

        if game.checkWin():
            return explored
        
        explored.append(child)
        # print(explored)
        successors = game.getFrontier()
        for s in successors:
            if not s in frontier and not s in explored:
                frontier.append(s)
        # print(frontier)
        
        
def dfsSolver(initialStateFile, goalStateFile, outputFile):
    print("hello world")

def iddfsSolver(initialStateFile, goalStateFile, outputFile):
    print("hello world")

def aStarSolver(initialStateFile, goalStateFile, outputFile):
    print("hello world")

def main():
    result = 0
    if sys.argv[3] == "bfs":
        result = bfsSolver(sys.argv[1], sys.argv[2], sys.argv[4])
    if sys.argv[3] == "dfs":
        result = dfsSolver(sys.argv[1], sys.argv[2], sys.argv[4])
    if sys.argv[3] == "iddfs":
        result = iddfsSolver(sys.argv[1], sys.argv[2], sys.argv[4])
    if sys.argv[3] == "astar":
        result = aStarSolver(sys.argv[1], sys.argv[2], sys.argv[4])

    if result == False:
        print("Could not find a solution")
    else:
        print(result)

if __name__ == "__main__":
    main()
