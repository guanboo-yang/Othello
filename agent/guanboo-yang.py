import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
from agent.base_agent import BaseAgent
import random

class MyAgent(BaseAgent):
    
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
        self.depth=10
        self.method=0   # method == 0 -> ABPruning last depth steps ; method == 1 -> ABPruning depth every steps

    def step(self, reward:dict, obs:dict) -> tuple:
        colorDict = {"black": -1, "white": 1, "empty": 0}
        colorNum = colorDict[self.color]
        
        def transfer(obsDict:dict) -> dict:
            '''
            obsDict: dict
                key: 0 ~ 63
                val: [-1, 0, 1] (black, empty, white)
            
            return : dict
                key: (x, y), where (7, 0) represents the top right
                val: [-1, 0, 1] (black, empty, white)
            '''
            return {(i % self.cols_n, i // self.cols_n):obsDict[i] for i in obsDict}
        
        obsNew=transfer(obs)    # new dictionary with 2D postion tuple keys
        
        def isOnBoard(x, y) -> bool:
            return 0 <= x < self.cols_n and 0 <= y < self.rows_n
        
        def isValidMove(obs:dict, move: tuple, color=colorNum) -> list:
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
        
        def makeMove(color, move, obs):
            tilesToFlip = isValidMove(obs, move, color)
            if tilesToFlip:
                obs[move] = color
                for tile in tilesToFlip:
                    obs[tile] = color
            return tilesToFlip
        
        # Corner position
        def isOnCorner(move):
            return move[0] in {0, self.cols_n-1} and move[1] in {0, self.rows_n-1}
        
        # Side position
        def isOnSide(move):
            return (move[0] in {0, self.cols_n-1} or move[1] in {0, self.rows_n-1}) and not isOnCorner(move)
        
        # change position
        def right(move):
            return (move[0]+1, move[1])
        def left(move):
            return (move[0]-1, move[1])
        def up(move):
            return (move[0], move[1]+1)
        def down(move):
            return (move[0], move[1]-1)
        
        # Side move is good or bad
        def isGoodSideMove(move, color) -> bool:
            obsTemp = obsNew.copy()
            if not isOnSide(move): return False
            makeMove(color, move, obsTemp)
            if move[1] in {0, self.rows_n-1}:
                lmove = rmove = move
                while not isOnCorner(lmove) and obsTemp[left(lmove)] == color: lmove = left(lmove)
                while not isOnCorner(rmove) and obsTemp[right(rmove)] == color: rmove = right(rmove)
                if isOnCorner(lmove) or isOnCorner(rmove): return True
                if obsTemp[left(lmove)] == -color and obsTemp[right(rmove)] == -color: return True
                if obsTemp[left(lmove)] == 0 and obsTemp[right(rmove)] == 0: 
                    lmove = left(lmove); rmove = right(rmove)
                    if isOnCorner(lmove) and isOnCorner(rmove): return True
                    if isOnCorner(lmove):
                        if obsTemp[right(rmove)] == color: return False
                        if obsTemp[right(rmove)] == -color: return True
                        else: return True
                    if isOnCorner(rmove):
                        if obsTemp[left(lmove)] == color: return False
                        if obsTemp[left(lmove)] == -color: return True
                        else: return True
                    if obsTemp[left(lmove)] == color or obsTemp[right(rmove)] == color: return False
                    if obsTemp[left(lmove)] == -color or obsTemp[right(rmove)] == -color: return True
                    else: return True
                else: return False
            else:
                umove = dmove = move
                while not isOnCorner(umove) and obsTemp[up(umove)] == color: umove = up(umove)
                while not isOnCorner(dmove) and obsTemp[down(dmove)] == color: dmove = down(dmove)
                if isOnCorner(umove) or isOnCorner(dmove): return True
                if obsTemp[up(umove)] == -color and obsTemp[down(dmove)] == -color: return True
                if obsTemp[up(umove)] == 0 and obsTemp[down(dmove)] == 0:
                    umove = up(umove); dmove = down(dmove)
                    if isOnCorner(umove) and isOnCorner(dmove): return True
                    if isOnCorner(umove):
                        if obsTemp[down(dmove)] == color: return False
                        if obsTemp[down(dmove)] == -color: return True
                        else: return True
                    if isOnCorner(dmove):
                        if obsTemp[up(umove)] == color: return False
                        if obsTemp[up(umove)] == -color: return True
                        else: return True
                    if obsTemp[up(umove)] == color or obsTemp[down(dmove)] == color: return False
                    if obsTemp[up(umove)] == -color or obsTemp[down(dmove)] == -color: return True
                    else: return True
                else: return False
        
        # X position
        def isBadMove(move, obs):
            if move == (1, 1) and obs[(0, 0)] == 0: return True
            if move == (1, self.rows_n-2) and obs[(0, self.rows_n-1)] == 0: return True
            if move == (self.cols_n-2, 1) and obs[(self.cols_n-1, 0)] == 0: return True
            if move == (self.cols_n-2, self.rows_n-2) and obs[(self.cols_n-1, self.rows_n-1)] == 0: return True
            else: return False
        # def isBadMove(move, obs):
        #     return move[0] in {1, self.cols_n-2} and move[1] in {1, self.rows_n-2}
        
        
        def getValidMovesDict(obs, color=colorNum) -> dict:
            return {(x, y):isValidMove(obs, (x, y), color) for x in range(self.cols_n) for y in range(self.rows_n) if isValidMove(obs, (x, y), color)}
        
        def getValidMovesList(obs, color=colorNum) -> list:
            return [(x, y) for x in range(self.cols_n) for y in range(self.rows_n) if isValidMove(obs, (x, y), color)]
        
        def countOpenRate(flip:tuple, obs:dict) -> int:
            count = 0
            dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            for xdir, ydir in dirs:
                x, y = flip[0]+xdir, flip[1]+ydir
                if isOnBoard(x, y) and obs[(x, y)] == 0:
                    count += 1
            return count
        
        def getScoreOfBoard(obs) -> dict:
            scores = {-1:0, 1:0}
            for i in obs:
                if obs[i] in scores:
                    scores[obs[i]] += 1
            return scores
        
        def isWinner(obs) -> int:
            scores = getScoreOfBoard(obs)
            # if scores[-1] > scores[1]: return -1
            # elif scores[-1] < scores[1]: return 1
            # else: return 0
            return scores[colorNum] - scores[-colorNum]
        
        def openRateDict(obs:dict, color) -> dict:
            validMovesDict = getValidMovesDict(obs, color)
            openRateDict = {}
            
            # try remove bad move
            for movek, movev in validMovesDict.copy().items():
                
                # don't flip X position
                for flip in movev:
                    obsFlipTest = obs.copy()
                    obsFlipTest[(movek)] = colorNum
                    if isBadMove(flip, obsFlipTest):
                        validMovesDict.pop(movek, None)
                        if validMovesDict == {}:
                            validMovesDict[movek] = movev
                
                # don't place X position
                if isBadMove(movek, obs):
                    validMovesDict.pop(movek, None)
                    if validMovesDict == {}:
                        validMovesDict[movek] = movev
                
                if isOnSide(movek) and not isGoodSideMove(movek, colorNum):
                    validMovesDict.pop(movek, None)
                    if validMovesDict == {}:
                        validMovesDict[movek] = movev
                
                # don't let the opponent play good move
                obsTest = obs.copy()
                opponentMovesbef = getValidMovesDict(obsTest, -colorNum)
                obsTest[(movek)] = colorNum
                opponentMovesaft = getValidMovesDict(obsTest, -colorNum)
                opponentMovesList = [i for i in opponentMovesaft if i not in opponentMovesbef]
                for move in opponentMovesList:
                    if isOnCorner(move):
                        validMovesDict.pop(movek, None)
                        if validMovesDict == {}:
                            validMovesDict[movek] = movev
            
            for move in validMovesDict:
                count = 0
                for flip in validMovesDict[move]:
                    count += countOpenRate(flip, obs)
                openRateDict[move] = count
            return openRateDict
        
        def hereIsPriority(obs, color):
            possibleMoves = list(openRateDict(obs, color).keys())
            # Corner position first
            for move in possibleMoves:
                if isOnCorner(move):
                    return move
            
            # Side position next
            for move in possibleMoves:
                if isGoodSideMove(move, colorNum):
                    return move
            
            return False
        
        def aßmaxNode(alpha, beta, height, color):
            bestop, bestScore = [-1,-1], alpha
            if height <= 0:
                bestScore = isWinner(obsAB)
                return bestop, bestScore
            elif not getValidMovesDict(obsAB, color):
                bestop, bestScore = aßminNode(alpha, beta, height-1, -color)
                return  [-1,-1], bestScore
            m = alpha
            moves = getValidMovesDict(obsAB, color)
            for move in moves:
                flips = makeMove(color, move, obsAB)
                _, score =aßminNode(m, beta, height-1, -color)

                obsAB[move] = 0
                otherTile = -color
                for tile in flips:
                    obsAB[tile] = otherTile

                if score > m:
                    m=score
                    bestop = move[:]
                    bestScore = m
                if m >= beta:
                    return bestop, bestScore
                return bestop, bestScore
        
        def aßminNode(alpha, beta, height, color):
            bestop, bestScore = [-1,-1], beta
            if height <= 0:
                bestScore = isWinner(obsAB)
                return bestop, bestScore
            elif not getValidMovesDict(obsAB, color):
                bestop, bestScore = aßmaxNode(alpha, beta, height-1, -color)
                return [-1,-1], bestScore
            m = beta
            moves = getValidMovesDict(obsAB, color)
            for move in moves:
                flips = makeMove(color, move, obsAB)
                _, score = aßmaxNode(alpha, m, height-1, -color)

                obsAB[move] = 0
                otherTile = -color
                for tile in flips:
                    obsAB[tile] = otherTile

                if score < m:
                    m=score
                    bestop = move[:]
                    bestScore = m
                if m <= alpha:
                    return bestop, bestScore
            return bestop, bestScore

        def getStaticValue(obs,color):
            sum=0
            # by weight
            for i in range(8):
                for j in range(8):
                    if (i>=2 and i<=5) and (j>=2 and j<=5):
                        sum+=color*obs[(i,j)]*(-1)
                    if ((i in (1,6)) and (j>=2 and j<=5) or (j in (1,6)) and (i>=2 and i<=5)):
                        sum+=color*obs[(i,j)]*(-2)
                    if ((i in (3,4)) and (j in (0,7)) or (j in (3,4)) and (i in (0,7))):
                        sum+=color*obs[(i,j)]*5
                    if ((i in (2,5)) and (j in (0,7)) or (j in (2,5)) and (i in (0,7))):
                        sum+=color*obs[(i,j)]*10
                    if ((i in (1,6)) and (j in (0,7)) or (j in (1,6)) and (i in (0,7))):
                        sum+=color*obs[(i,j)]*(-20)
                    if ((i,j) in ((0,0),(0,7),(7,0),(7,7))):
                        sum+=color*obs[(i,j)]*100
                    if ((i,j) in ((1,1),(1,6),(6,1),(6,6))):
                        sum+=color*obs[(i,j)]*(-50)
            # by score
            score=isWinner(obs)
            return sum

        def ABPruning(alpha,beta,depth,color,obs,maximize):
            if depth<=0:
                if self.method == 0:
                    return [-1,-1], isWinner(obs)
                elif self.method == 1:
                    return [-1,-1], getStaticValue(obs,color)
            elif not getValidMovesDict(obs,color):
                return [-1,-1],ABPruning(alpha,beta,depth-2,color,obs,maximize)[1]
            if maximize:
                maxEval = -float('inf')
                moves = getValidMovesDict(obs,color)
                bestOp=[-1,-1]
                for move in moves:
                    obsAB=obs.copy()
                    flips=makeMove(color,move,obsAB)
                    for toFlip in flips:
                        obsAB[toFlip]=color
                    evaluate=ABPruning(alpha,beta,depth-1,-color,obsAB,False)[1]
                    # maxEval = max(maxEval, evaluatate)
                    if evaluate>maxEval:
                        maxEval = evaluate
                        bestOp = move[:]
                    alpha=max(alpha,evaluate)
                    if beta <= alpha:
                        break
                return bestOp,maxEval
            else:
                minEval = float('inf')
                moves = getValidMovesDict(obs,color)
                bestOp=[-1,-1]
                for move in moves:
                    obsAB=obs.copy()
                    flips=makeMove(color,move,obsAB)
                    for toFlip in flips:
                        obsAB[toFlip]=color
                    evaluate=ABPruning(alpha,beta,depth-1,-color,obsAB,True)[1]
                    if minEval>evaluate:
                        minEval=evaluate
                        bestOp=move[:]
                    beta=min(beta,evaluate)
                    if beta <= alpha:
                        break
                return bestOp, minEval

        def miniMax(depth,color,obs,maximize):
            if depth<=0:
                return [-1,-1], isWinner(obs)
            elif not getValidMovesDict(obs,color):
                return [-1,-1],miniMax(depth-2,color,obs,maximize)[1]
            if maximize:
                maxEval = -float('inf')
                moves = getValidMovesDict(obs,color)
                bestOp=[-1,-1]
                for move in moves:
                    obsAB=obs.copy()
                    flips=makeMove(color,move,obsAB)
                    for toFlip in flips:
                        obsAB[toFlip]=color
                    evaluate=miniMax(depth-1,-color,obsAB,False)[1]
                    # maxEval = max(maxEval, evaluatate)
                    if evaluate>maxEval:
                        maxEval = evaluate
                        bestOp = move[:]
                print(maxEval)
                return bestOp,maxEval
            else:
                minEval = float('inf')
                moves = getValidMovesDict(obs,color)
                bestOp=[-1,-1]
                for move in moves:
                    obsAB=obs.copy()
                    flips=makeMove(color,move,obsAB)
                    for toFlip in flips:
                        obsAB[toFlip]=color
                    evaluate=miniMax(depth-1,-color,obsAB,True)[1]
                    if minEval>evaluate:
                        minEval=evaluate
                        bestOp=move[:]
                print(minEval)
                return bestOp, minEval

        def getComputerMove(agentColor):
            if agentColor == 1:
                move, _ = aßmaxNode(-99, 99, self.depth, agentColor)
            else:
                move, _ = aßminNode(-99, 99, self.depth, agentColor)
            return move
        
        def getComputerMoveN(agentColor,obs):
            if agentColor == 1:
                return ABPruning(-99,99,self.depth,agentColor,obs,True)[0]
            else:
                return ABPruning(-99,99,self.depth,agentColor,obs,False)[0]

        def countSteps(obs):
            step = 0
            for i in obs:
                if obs[i] != 0:
                    step += 1
            return step
        
        stepNum = countSteps(obsNew)
        
        if stepNum == 5 and self.method==0:
            for move in [(2, 2), (5, 5)]:
                if isValidMove(obsNew, move, colorNum):
                    x, y = move
            return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

        
        elif stepNum <= 63-self.depth and self.method==0:
            # rondom choice
            MovesDict = openRateDict(obsNew, colorNum)
            keys = list(MovesDict.keys())
            random.shuffle(keys)
            randomDict = {key:MovesDict[key] for key in keys}
            
            # sorted with openrate
            sortedOpenRateDict = {k:v for k, v in sorted(randomDict.items(), key=lambda x: x[1])}
            try: x, y = next(iter(sortedOpenRateDict))
            except StopIteration: return
            
            # priority move
            if hereIsPriority(obsNew, colorNum):
                x, y = hereIsPriority(obsNew, colorNum)
            
            return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT
        
        else:
            obsAB = obsNew.copy()
            #x, y = getComputerMove(colorNum)
            x,y=ABPruning(-float('inf'),float('inf'),self.depth,colorNum,obsAB,True)[0]
            #x,y=miniMax(self.depth,colorNum,obsAB,True)[0]
            return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

class RandomAgent(BaseAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
    
    def step(self, reward:dict, obs:dict) -> tuple:
        colorDict = {"black": -1, "white": 1, "empty": 0}
        colorNum = colorDict[self.color]
        
        def transfer(obsDict:dict) -> dict:
            '''
            obsDict: dict
                key: 0 ~ 63
                val: [-1, 0, 1] (black, empty, white)
            
            return : dict
                key: (x, y), where (7, 0) represents the top right
                val: [-1, 0, 1] (black, empty, white)
            '''
            return {(i % self.cols_n, i // self.cols_n):obsDict[i] for i in obsDict}
        
        obsNew=transfer(obs)    # new dictionary with 2D postion tuple keys
        
        def isOnBoard(x, y) -> bool:
            return 0 <= x < self.cols_n and 0 <= y < self.rows_n
        
        def isValidMove(obs:dict, move: tuple, color=colorNum) -> list:
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
        
        def getValidMovesList(obs, color=colorNum) -> list:
            return [(x, y) for x in range(self.cols_n) for y in range(self.rows_n) if isValidMove(obs, (x, y), color)]
        
        possibleMoves = getValidMovesList(obsNew)
        random.shuffle(possibleMoves)
        x, y = possibleMoves[0]
        return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

class CornerAgent(BaseAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
    
    def step(self, reward:dict, obs:dict) -> tuple:
        colorDict = {"black": -1, "white": 1, "empty": 0}
        colorNum = colorDict[self.color]
        
        def transfer(obsDict:dict) -> dict:
            '''
            obsDict: dict
                key: 0 ~ 63
                val: [-1, 0, 1] (black, empty, white)
            
            return : dict
                key: (x, y), where (7, 0) represents the top right
                val: [-1, 0, 1] (black, empty, white)
            '''
            return {(i % self.cols_n, i // self.cols_n):obsDict[i] for i in obsDict}
        
        obsNew=transfer(obs)    # new dictionary with 2D postion tuple keys
        
        def isOnBoard(x, y) -> bool:
            return 0 <= x < self.cols_n and 0 <= y < self.rows_n
        
        def isValidMove(obs:dict, move: tuple, color=colorNum) -> list:
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
        
        def getValidMovesList(obs, color=colorNum) -> list:
            return [(x, y) for x in range(self.cols_n) for y in range(self.rows_n) if isValidMove(obs, (x, y), color)]
        
        # Corner position
        def isOnCorner(move):
            return move[0] in {0, self.cols_n-1} and move[1] in {0, self.rows_n-1}
        
        # X position
        def isBadMove(move, obs):
            if move == (1, 1) and obs[(0, 0)] == 0: return True
            if move == (1, self.rows_n-2) and obs[(0, self.rows_n-1)] == 0: return True
            if move == (self.cols_n-2, 1) and obs[(self.cols_n-1, 0)] == 0: return True
            if move == (self.cols_n-2, self.rows_n-2) and obs[(self.cols_n-1, self.rows_n-1)] == 0: return True
            else: return False
        
        possibleMoves = getValidMovesList(obsNew)
        random.shuffle(possibleMoves)
        for move in possibleMoves:
            if isBadMove(move, obsNew):
                possibleMoves.remove(move)
                possibleMoves.append(move)
        x, y = possibleMoves[0]
        for move in possibleMoves:
            if isOnCorner(move):
                x, y = move
        return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

class MyAgent1(MyAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
        self.depth=5
        self.method=1
    