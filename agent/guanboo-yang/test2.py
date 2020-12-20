def sideMoveLevel(move, color, obs) -> int:
    def pine(obs):
        a = obs.values()
        ll = []
        for i in range(8):
            ll.append(list(a)[8*i:8*i+8])
        for x in range(8):
            for y in range(8):
                if ll[x][y] == -1: ll[x][y] = 2
        for i in range(8):
            print(*ll[i])
    obsTemp = obs.copy()
    # if obsTemp[move] != 0: return False
    if not isOnSide(move): return 5
    flips = makeMove(color, move, obsTemp)
    for flip in flips:
        if isBadMove(flip, obsTemp): return 5
    func = [right, left] if move[1] in {0, 7} else [up, down]
    moves = [move, move]
    while not isOnCorner(moves[0]) and obsTemp[func[0](moves[0])] == color: moves[0] = func[0](moves[0])
    while not isOnCorner(moves[1]) and obsTemp[func[1](moves[1])] == color: moves[1] = func[1](moves[1])
    # print(moves)
    if isOnCorner(moves[0]) or isOnCorner(moves[1]): return 2
    if obsTemp[func[0](moves[0])] == -color and obsTemp[func[1](moves[1])] == -color: return 3
    if obsTemp[func[0](moves[0])] == 0 and obsTemp[func[1](moves[1])] == 0: 
        moves[0] = func[0](moves[0]); moves[1] = func[1](moves[1])
        if isOnCorner(moves[0]) and isOnCorner(moves[1]):
            for flip in flips:
                if isOnSide(flip): return 1
            else: return 3
        if sideMoveLevel(moves[0], -color, obsTemp) == 3: return 4
        if sideMoveLevel(moves[0], -color, obsTemp) <= 2: return 5
        if sideMoveLevel(moves[1], -color, obsTemp) == 3: return 4
        if sideMoveLevel(moves[1], -color, obsTemp) <= 2: return 5
        else:
            for flip in flips:
                if isOnSide(flip): return 1
            else: return 3
    else:
        i = 1 if (obsTemp[func[0](moves[0])] == -color) else 0
        if isOnCorner(func[i](moves[i])): return 5
        if (sideMoveLevel(func[i](moves[i]), -color, obsTemp) == 5): return 2
        if (sideMoveLevel(func[i](moves[i]), -color, obsTemp) == 3): return 4
        if (sideMoveLevel(func[i](moves[i]), -color, obsTemp) <= 2): return 5
        else: return 3

obs =  {(0, 0):  0, (0, 1):  0, (0, 2):  1, (0, 3):  1, (0, 4):  0, (0, 5): -1, (0, 6): -1, (0, 7):  0, 
        (1, 0):  0, (1, 1):  0, (1, 2): -1, (1, 3): -1, (1, 4):  1, (1, 5): -1, (1, 6):  0, (1, 7):  0, 
        (2, 0):  1, (2, 1):  1, (2, 2): -1, (2, 3): -1, (2, 4): -1, (2, 5):  1, (2, 6):  0, (2, 7): -1, 
        (3, 0):  0, (3, 1): -1, (3, 2): -1, (3, 3):  1, (3, 4): -1, (3, 5):  1, (3, 6):  0, (3, 7):  0, 
        (4, 0): -1, (4, 1): -1, (4, 2): -1, (4, 3):  1, (4, 4):  1, (4, 5):  1, (4, 6):  0, (4, 7):  1, 
        (5, 0): -1, (5, 1): -1, (5, 2):  1, (5, 3): -1, (5, 4):  1, (5, 5):  1, (5, 6): -1, (5, 7):  1, 
        (6, 0): -1, (6, 1):  0, (6, 2):  1, (6, 3):  1, (6, 4): -1, (6, 5):  1, (6, 6):  1, (6, 7): -1, 
        (7, 0):  0, (7, 1): -1, (7, 2): -1, (7, 3):  0, (7, 4):  0, (7, 5):  0, (7, 6):  0, (7, 7):  0}

def isStonerSide(obsIN, color):
    def stonerWrapper(obs, color, move, funcList):
        obs = obsIN.copy()
        if obs[move] != 0: return False
        returnVal = funcList[0](funcList[1](move))
        if not isValidMove(obs, returnVal, color): return False
        if obs[funcList[0](funcList[1](move))] != 0: return False
        _ = makeMove(color, returnVal, obs)
        if funcList[1](move) not in getValidMovesDict(obs, -color): return False
        print(getValidMovesDict(obs, -color)[funcList[1](move)])
        if not any(returnVal in sublist for sublist in getValidMovesDict(obs, -color)[funcList[1](move)]): return False
        if diagWithSameColor(obs, color, move):
            moveEnd = funcList[1](funcList[1](funcList[1](funcList[1](funcList[1](funcList[1](funcList[1](move)))))))
            if obs[moveEnd] != 0: return False
            moveEnd = funcList[2](moveEnd)
            while obs[moveEnd] == -color: moveEnd = funcList[2](moveEnd)
            if obs[moveEnd] == 0: moveEnd = funcList[2](moveEnd)
            else: return False
            while obs[moveEnd] == color: moveEnd = funcList[2](moveEnd)
            if obs[moveEnd] != 0: return False
            if funcList[2](moveEnd) != move: return False
            return returnVal
        else: return False
    Xlist = []
    Xlist.append(stonerWrapper(obs, color, (0, 0), [right, down, up]))
    Xlist.append(stonerWrapper(obs, color, (0, 0), [down, right, left]))
    Xlist.append(stonerWrapper(obs, color, (7, 0), [down, left, right]))
    Xlist.append(stonerWrapper(obs, color, (7, 0), [left, down, up]))
    Xlist.append(stonerWrapper(obs, color, (7, 7), [left, up, down]))
    Xlist.append(stonerWrapper(obs, color, (7, 7), [up, left, right]))
    Xlist.append(stonerWrapper(obs, color, (0, 7), [up, right, left]))
    Xlist.append(stonerWrapper(obs, color, (0, 7), [right, up, down]))
    # print(Xlist)
    for move in Xlist:
        if move != False:
            return move
    else: return False
    
    # moves = [(0, 0), (0, 7), (7, 0), (7, 7)]
    # funcs = [[right, down], [right, up], [left, down], [left, up]]
    # for i in range(4):
    #     returnMove1 = funcs[i][0](funcs[i][1](moves[i]))
    #     if obs[moves[i]] == 0:
    #         for func in funcs[i]:
    #             move = func(moves[i])
    #             returnMove2 = move
    #             if obs[move] == 0:
    #                 move = func(move)
    #                 while obs[move] == color: move = func(move)
    #                 if obs[move] == 0: move = func(move)
    #                 while obs[move] == -color: move = func(move)
    #                 if isOnCorner(func(move)): 
    #                     x, y = returnMove1, returnMove2
    
    
    # for move in [(0, 0), (0, 7), (7, 0), (7, 7)]:
    #     func = 
    #     if obs[move] == 0:
    #         for func in [right, left, up, down]:
    #             if isOnBoard(func(move)) and obs[func(move)] == 0:
    #                 move = func(move)
    #                 returnMove = move
    #                 while obs[move] == color: move = func(move)
    #                 if obs[move] == 0: move = func(move)
    #                 while obs[move] == -color: move = func(move)
    #                 if isOnCorner(func(move)): return returnMove

# def stoner(obs, color):
#     pos = isStonerSide(obs, color)
#     if pos:
        

# def pine(obs):
#     a = obs.values()
#     ll = []
#     for i in range(8):
#         ll.append(list(a)[8*i:8*i+8])
#     for x in range(8):
#         for y in range(8):
#             if ll[x][y] == -1: ll[x][y] = 2
#     for i in range(8):
#         print(*ll[i])

# pine(obs)

# Get legal moves
def getValidMovesDict(obs, color) -> dict:
    return {(x, y):isValidMove(obs, (x, y), color) for x in range(8) for y in range(8) if isValidMove(obs, (x, y), color)}

def diagWithSameColor(obs, color, move):
    if move[0] == move[1]:
        return all(obs[(x, y)] != -color for x in range(1, 7) for y in range(1, 7) if x == y)
    if move[0] + move[1] == 7:
        return all(obs[(x, y)] != -color for x in range(1, 7) for y in range(1, 7) if x + y == 7)

def makeMove(color, move, obs):
    tilesToFlip = isValidMove(obs, move, color)
    obs[move] = color
    for tile in tilesToFlip:
        obs[tile] = color
    return tilesToFlip

# directions
def right(move):
    return (move[0]+1, move[1])

def left(move):
    return (move[0]-1, move[1])

def up(move):
    return (move[0], move[1]-1)

def down(move):
    return (move[0], move[1]+1)

# Corner position
def isOnCorner(move):
    return move[0] in {0, 7} and move[1] in {0, 7}

# Side position
def isOnSide(move):
    return (move[0] in {0, 7} or move[1] in {0, 7}) and not isOnCorner(move)

# X position
def isBadMove(move, obs):
    if move == (1, 1) and obs[(0, 0)] == 0: return True
    if move == (1, 8-2) and obs[(0, 7)] == 0: return True
    if move == (8-2, 1) and obs[(7, 0)] == 0: return True
    if move == (8-2, 8-2) and obs[(7, 7)] == 0: return True
    else: return False

def isValidMove(obs:dict, move: tuple, color) -> list:
    if not isOnBoard(move[0], move[1]) or obs[(move[0], move[1])] != 0:
        return []
    obs[(move[0], move[1])] = color
    dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    tilesToFlip = []
    for xdir, ydir in dirs:
        x, y = move[0]+xdir, move[1]+ydir
        while isOnBoard(x, y) and obs[(x, y)] == -color:
            x += xdir; y += ydir
            if isOnBoard(x, y) and obs[(x, y)] == color:
                while True:
                    x -= xdir; y -= ydir
                    if x == move[0] and y == move[1]:
                        break
                    tilesToFlip.append((x, y))
    obs[(move[0], move[1])] = 0
    return tilesToFlip

def pineapple(obs):
    a = obs.values()
    for i in range(8):
        print((list(a)[8*i:8*i+8]))

def isOnBoard(x, y) -> bool:
    return 0 <= x < 8 and 0 <= y < 8

# colorNum, x, y = [int(i) for i in input().split()]
# print(sideMoveLevel((x, y), colorNum, obs))

colorNum = int(input())
print(isStonerSide(obs, colorNum))


    #     if isOnCorner(moves[0]):
    #         if obsTemp[func[1](moves[1])] == color: return False
    #         if obsTemp[func[1](moves[1])] == -color: return True
    #         else: return True
    #     if isOnCorner(moves[1]):
    #         if obsTemp[func[0](moves[0])] == color: return False
    #         if obsTemp[func[0](moves[0])] == -color: return True
    #         else: return True
    #     if obsTemp[func[0](moves[0])] == color or obsTemp[func[1](moves[1])] == color: return False
    #     if obsTemp[func[0](moves[0])] == -color or obsTemp[func[1](moves[1])] == -color: return True
    #     else: return True
    # else:
    #     if obsTemp[func[0](moves[0])] == -color:
    #         if sideMoveLevel(func[1](moves[1]), -color, obsTemp) or isOnCorner(func[1](moves[1])): return False
    #         else: return True
    #     if obsTemp[func[1](moves[1])] == -color:
    #         if sideMoveLevel(func[0](moves[0]), -color, obsTemp) or isOnCorner(func[0](moves[0])): return False
    #         else: return True