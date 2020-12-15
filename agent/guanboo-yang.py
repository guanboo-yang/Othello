import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
from agent.base_agent import BaseAgent
import random

class MyAgent(BaseAgent):
    
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
        self.depth = 0
    
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
        
        def fakeMakeMove(color, move, obs):
            tilesToFlip = isValidMove(obs, move, color)
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
        
        def sideMoveLevel(move, color, obs) -> int:
            obsTemp = obs.copy()
            if obsTemp[move] != 0: return False
            if not isOnSide(move): return 5
            flips = fakeMakeMove(color, move, obsTemp)
            for flip in flips:
                if isBadMove(flip, obsTemp): return 5
            func = [right, left] if move[1] in {0, 7} else [up, down]
            moves = [move, move]
            while not isOnCorner(moves[0]) and obsTemp[func[0](moves[0])] == color: moves[0] = func[0](moves[0])
            while not isOnCorner(moves[1]) and obsTemp[func[1](moves[1])] == color: moves[1] = func[1](moves[1])
            if isOnCorner(moves[0]) or isOnCorner(moves[1]): return 2
            if obsTemp[func[0](moves[0])] == -color and obsTemp[func[1](moves[1])] == -color: return 3
            if obsTemp[func[0](moves[0])] == 0 and obsTemp[func[1](moves[1])] == 0: 
                moves[0] = func[0](moves[0]); moves[1] = func[1](moves[1])
                if isOnCorner(moves[0]) and isOnCorner(moves[1]):
                    for flip in flips:
                        if isOnSide(flip): return 1
                    else: return 3
                if sideMoveLevel(moves[0], -color, obsTemp) <= 3: return 4
                if sideMoveLevel(moves[1], -color, obsTemp) <= 3: return 4
                else:
                    for flip in flips:
                        if isOnSide(flip): return 1
                    else: return 3
            else:
                i = 1 if obsTemp[func[0](moves[0])] == -color else 0
                if isOnCorner(func[i](moves[i])): return 5
                if (sideMoveLevel(func[i](moves[i]), -color, obsTemp) <= 3): return 4
                else: return 3
        
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
            return scores[1] - scores[-1]
        
        def actionCap(move, color):
            obsCap = obsNew.copy()
            _ = makeMove(color, move, obsCap)
            agentMove = len(getValidMovesList(obsCap, color))
            opponentMove = len(getValidMovesList(obsCap, -color))
            actionVal = agentMove - opponentMove
            return actionVal
        
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
                
                if isOnSide(movek) and sideMoveLevel(movek, color, obs) == 5:
                    validMovesDict.pop(movek, None)
                    if validMovesDict == {}:
                        validMovesDict[movek] = movev
                
                if isOnSide(movek) and sideMoveLevel(movek, color, obs) == 4:
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
                count -= actionCap(move, color) * 0.2
                openRateDict[move] = count
            return openRateDict
        
        def hereIsPriority(obs, color):
            possibleMoves = getValidMovesList(obs, color)
            # Corner position first
            for move in possibleMoves:
                if isOnCorner(move):
                    return move
            
            # Side position next
            for move in possibleMoves:
                if isOnSide(move) and sideMoveLevel(move, color, obs) == 1:
                    return move
                if isOnSide(move) and sideMoveLevel(move, color, obs) == 2:
                    return move
                if isOnSide(move) and sideMoveLevel(move, color, obs) == 3:
                    return move
            
            return False
        
        def minimax(height, color, obs):
            obsMM = obs.copy()
            if color == -1:
                bestOp, bestScore = (-1, -1), 99
                if height <= 0:
                    bestScore = isWinner(obsMM)
                    return bestOp, bestScore
                elif not getValidMovesDict(obsMM, color):
                    bestOp, bestScore = minimax(height-1, -color, obsMM)
                    return  (-1,-1), bestScore
                moves = getValidMovesDict(obsMM, color)
                for move in moves:
                    _ = makeMove(color, move, obsMM)
                    _, score = minimax(height-1, -color, obsMM)
                    if score < bestScore:
                        bestScore = score
                        bestOp = move[:]
                return bestOp, bestScore
            if color == 1:
                bestOp, bestScore = (-1, -1), -99
                if height <= 0:
                    bestScore = isWinner(obsMM)
                    return bestOp, bestScore
                elif not getValidMovesDict(obsMM, color):
                    bestOp, bestScore = minimax(height-1, -color, obsMM)
                    return  (-1,-1), bestScore
                moves = getValidMovesDict(obsMM, color)
                for move in moves:
                    _ = makeMove(color, move, obsMM)
                    _, score = minimax(height-1, -color, obsMM)
                    if score > bestScore:
                        bestScore = score
                        bestOp = move[:]
                return bestOp, bestScore
        
        def countSteps(obs):
            step = 0
            for i in obs:
                if obs[i] != 0:
                    step += 1
            return step
        
        stepNum = countSteps(obsNew)
        
        if stepNum == 5:
            for move in [(2, 2), (5, 5)]:
                if isValidMove(obsNew, move, colorNum):
                    x, y = move
            return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

        
        elif stepNum <= (63 - self.depth):
            # rondom choice
            MovesDict = openRateDict(obsNew, colorNum)
            keys = list(MovesDict.keys())
            random.shuffle(keys)
            randomDict = {key:MovesDict[key] for key in keys}
            
            # sorted with openrate
            sortedOpenRateDict = {k:v for k, v in sorted(randomDict.items(), key=lambda x: x[1])}
            # print(sortedOpenRateDict)
            try: x, y = next(iter(sortedOpenRateDict))
            except StopIteration: return
            
            # priority move
            priorityMoves = hereIsPriority(obsNew, colorNum)
            # print(priorityMoves)
            if priorityMoves:
                x, y = priorityMoves
            
            return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT
        
        else:
            x, y = minimax(self.depth, colorNum, obsNew)[0]
            return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT


class RandomAgent(BaseAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
    
    def step(self, reward:dict, obs:dict) -> tuple:
        colorDict = {"black": -1, "white": 1, "empty": 0}
        colorNum = colorDict[self.color]
        
        def transfer(obsDict:dict) -> dict:
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
        try: x, y = possibleMoves[0]
        except: return
        return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

class CornerAgent(BaseAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
    
    def step(self, reward:dict, obs:dict) -> tuple:
        colorDict = {"black": -1, "white": 1, "empty": 0}
        colorNum = colorDict[self.color]
        
        def transfer(obsDict:dict) -> dict:
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
        try: x, y = possibleMoves[0]
        except: return
        for move in possibleMoves:
            if isOnCorner(move):
                x, y = move
        return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

class MyAgent2(MyAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
        self.depth = 5
    
class MyAgent3(MyAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
        self.depth = 10
    
class MyAgent4(MyAgent):
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        super().__init__(color, rows_n, cols_n, width, height)
        self.depth = 15
