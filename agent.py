import updatewumpusNowWithRocks
import FOPC

#instead of using a dictionary of a dictionary for the knowledge base
#we used a cell class and made a dictionary of these objects
class cell:
    def __init__(self, wumpus = 0, pit = 0, visited = False, numVisited = 0, safe =False, neighbors = None, deadEnd = False, leaving = False):
        self.wumpus = wumpus
        self.pit = pit
        self.visited = visited
        self.numVisited = numVisited
        self.safe = safe
        self.neighbors = neighbors
        self.deadEnd = deadEnd
        self.leaving = leaving



goldFound = False
wampusDead = False
blockades = 0

#create and return a dictionary of cell objects to populate the knowledge base
def createBoardWithCellRepresentation():
    layout = {}
    height = 4
    width = 4
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            layout["Cell "+str(x)+str(y)] = {}
            layout["Cell "+str(x)+str(y)]["cellInfo"] = cell(wumpus=0,pit=0,visited=False, numVisited=0, safe=False, neighbors=None, deadEnd = False, leaving = False)
    return layout


#kb stands for knowledgebase
name = updatewumpusNowWithRocks.intialize_world()
#name = updatewumpusNowWithRocks.intialize_my_world("Cell 44", "Cell 34", ["Cell 14", "Cell 23", "Cell 32"])

bindings = {}
kb = createBoardWithCellRepresentation()
kb["Cell 11"]["cellInfo"].visited = True
kb["Cell 11"]["cellInfo"].safe = True
kb["Cell 11"]["cellInfo"].numVisited += 1
moves = ["Cell 11"]

#Perceptions are:
#[Stench, Breeze, Glitter, Bump, WoefulScream]
#update the kb using these perceptions
def updateKB(perceptions):
    cellName = perceptions[5]
    #var = kb.get([cellName]["cellInfo"].visited, False)
    kb[cellName]["cellInfo"].numVisited += 1
    if kb[cellName]["cellInfo"].visited == False:
        kb[cellName]["cellInfo"].neighbors = updatewumpusNowWithRocks.look_ahead(name)
        kb[cellName]["cellInfo"].safe = True
        kb[cellName]["cellInfo"].visited = True
        for i in range(0, 5):
            statement = (perceptions[i], cellName)
            pattern = (perceptions[i], "?" + cellName)
            match = FOPC.match(statement, pattern, bindings)
            data = (FOPC.instantiate(statement, match))
            kb[cellName][data[0]] = data[1]
    inferenceEngine(perceptions)
    optimalMove = findMove(perceptions)
    perceptions2 = makeMove(cellName, optimalMove)
    score = perceptions2[8]
    if score >= 1100:
        checkWinPerceptions = goHome(perceptions2[5])
        if checkWinPerceptions[7] == "won":
            return "Game won"

    return updateKB(perceptions2)


def inferenceEngine(perceptions):
    global blockades
    surroundings = updatewumpusNowWithRocks.look_ahead(name)
    unsafeMoves = []
    for neighbor in surroundings:
        if kb[neighbor]["cellInfo"].safe == False:
            unsafeMoves.append(neighbor)


    if perceptions[1] is not 'breeze' and perceptions[0] is not 'nasty':
        for i in range(0,len(unsafeMoves)):
            kb[unsafeMoves[i]]["cellInfo"].wumpus += -10
            kb[unsafeMoves[i]]["cellInfo"].pit += -10

    if perceptions[1] == 'breeze' and perceptions[0] == 'clean' and blockades < 3:
        for i in range(0,len(unsafeMoves)):
            kb[unsafeMoves[i]]["cellInfo"].wumpus += -10
            kb[unsafeMoves[i]]["cellInfo"].pit += 1

    if perceptions[1] is not 'breeze' and perceptions[0] == 'nasty':
        for i in range(0,len(unsafeMoves)):
            kb[unsafeMoves[i]]["cellInfo"].wumpus += 1
            kb[unsafeMoves[i]]["cellInfo"].pit += -10

    if perceptions[1] == 'breeze' and perceptions[0] == 'nasty' and blockades < 3:
        for i in range(0,len(unsafeMoves)):
            kb[unsafeMoves[i]]["cellInfo"].wumpus += 1
            kb[unsafeMoves[i]]["cellInfo"].pit += 1

    x = kb
    for unsafeCell in unsafeMoves:
        if kb[unsafeCell]["cellInfo"].wumpus < 0 and kb[unsafeCell]["cellInfo"].pit < 0:
            kb[unsafeCell]["cellInfo"].safe = True



def findMove(perceptions):
    global blockades
    currentCell = perceptions[5]
    neighbors = updatewumpusNowWithRocks.look_ahead(name)
    safeMoves = []
    dangerousMoves = []
    optimalMoves = []
    x = kb
    for move in neighbors:
        if kb[move]["cellInfo"].safe is True:
            safeMoves.append(move)
        else:
            dangerousMoves.append(move)
    if blockades < 3:
        if len(safeMoves) is 1 and kb[currentCell]["cellInfo"].numVisited > 1:
            stuck = throwRocks(currentCell, dangerousMoves)
            if stuck == True:
                kb[currentCell]["cellInfo"].deadEnd = True
            else:
                for move in dangerousMoves:
                    if kb[currentCell]["cellInfo"].safe == True:
                        safeMoves.append(move)

    for move in safeMoves:
        if kb[move]["cellInfo"].visited is False:
            optimalMoves.append(move)

    if len(optimalMoves) == 0:
        bestOptimumMove = safeMoves[0]
        for move in safeMoves:
            if kb[move]["cellInfo"].numVisited < kb[bestOptimumMove]["cellInfo"].numVisited and kb[move]["cellInfo"].deadEnd == False:
                bestOptimumMove = move
        return bestOptimumMove
    else:
        return optimalMoves[0]


def makeMove(currentCell, desiredCell):
    x = kb
    wumpusNear = False
    if "glitter" in kb[currentCell]:
        perceptions = updatewumpusNowWithRocks.take_action(name, "PickUp")
        del kb[currentCell]["glitter"]
        return perceptions

    neighbors = updatewumpusNowWithRocks.look_ahead(name)
    global wampusDead
    for move in neighbors:
        if kb[move]["cellInfo"].wumpus >= 2 and wampusDead == False:
            desiredCell = move
            wumpusNear = True
    if wumpusNear == True and wampusDead == False:
        orientSelf(currentCell, desiredCell)
        perceptions = updatewumpusNowWithRocks.take_action(name, "Shoot")
        wampusDead = True
        kb[desiredCell]["cellInfo"].safe = True
        kb[desiredCell]["cellInfo"].visited = True
        kb[desiredCell]["cellInfo"].numVisited += 1
        if "nasty" in kb[currentCell]:
            del kb[currentCell]["nasty"]
        return perceptions

    orientSelf(currentCell,desiredCell)
    return updatewumpusNowWithRocks.take_action(name, "Step")


def orientSelf(currentCel, desiredCell):
    xdiff = int(currentCel[5]) - int(desiredCell[5])
    ydiff = int(currentCel[6]) - int(desiredCell[6])
    if ydiff == -1:
        updatewumpusNowWithRocks.take_action(name, "Up")
    elif ydiff == 1:
        updatewumpusNowWithRocks.take_action(name, "Down")
    elif xdiff == 1:
        updatewumpusNowWithRocks.take_action(name, "Left")
    elif xdiff == -1:
        updatewumpusNowWithRocks.take_action(name, "Right")

def throwRocks(currentCell, dangerousMoves):
    global blockades
    pitCount = 0
    if "breeze" in kb[currentCell]:
        for move in dangerousMoves:
            desiredCell = move
            orientSelf(currentCell, desiredCell)
            perceptionGained = updatewumpusNowWithRocks.take_action(name, "Toss")
            if perceptionGained == "Clink":
                pitCount += 1
                kb[desiredCell]["cellInfo"].safe = True
                perceptionGained = ""
            else:
                kb[desiredCell]["cellInfo"].pit = float("infinity")
                blockades += 1
    if pitCount == 0:
        return True
    else:
        return False

def goHome(currentCell):
    if currentCell == "Cell 11":
        perception = updatewumpusNowWithRocks.take_action(name, "Exit")
        return perception
    else:
        x = kb
        neighbors = updatewumpusNowWithRocks.look_ahead(name)
        safeMoves = []
        for move in neighbors:
            xdiff = int(move[5]) - int(currentCell[5])
            ydiff = int(move[6]) - int(currentCell[6])
            if xdiff == -1 or ydiff == -1:
                if kb[move]["cellInfo"].safe == True:
                    if kb[move]["cellInfo"].leaving == False:
                        safeMoves.append(move)

        if len(safeMoves) == 0:
            for move in neighbors:
                if kb[move]["cellInfo"].safe == True:
                    if kb[move]["cellInfo"].leaving == False:
                        desiredcell = move
                        kb[desiredcell]["cellInfo"].leaving = True
                        break
        else:
            desiredcell = safeMoves[0]
            kb[desiredcell]["cellInfo"].leaving = True

        orientSelf(currentCell,desiredcell)
        newPerceptions = updatewumpusNowWithRocks.take_action(name,"Step")
        return goHome(newPerceptions[5])


perceptions = updatewumpusNowWithRocks.take_action(name, "Step")
updateKB(perceptions)
