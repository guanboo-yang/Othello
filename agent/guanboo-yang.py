import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
from agent.base_agent import BaseAgent, RandomAgent, HumanAgent

class MyAgent(BaseAgent):
    
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
        
        def isValidMove(obs:dict, move: tuple) -> list:
            if not isOnBoard(move[0], move[1]) or obs[(move[0], move[1])] != 0:
                return []
            obs[(move[0], move[1])] = colorNum
            dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            tilesToFlip = []
            for xdir, ydir in dirs:
                x, y = move[0]+xdir, move[1]+ydir
                while isOnBoard(x, y) and obs[(x, y)] == -colorNum:
                    x += xdir; y += ydir
                    if isOnBoard(x, y) and obs[(x, y)] == colorNum:
                        while True:
                            x -= xdir; y -= ydir
                            if x == move[0] and y == move[1]:
                                break
                            tilesToFlip.append((x, y))
            obs[(move[0], move[1])] = 0
            return tilesToFlip
        
        def getValidMoves(obs) -> list:
            return [(x, y) for x in range(self.cols_n) for y in range(self.rows_n) if isValidMove(obs, (x, y))]
        
        # Corner position
        def isOnCorner(move):
            return move[0] in {0, self.cols_n-1} and move[1] in {0, self.rows_n-1}
        
        # Side position
        def isOnSide(move):
            return move[0] in {0, self.cols_n-1} or move[1] in {0, self.rows_n-1}
        
        # C position
        def isBadMove(move):
            return move[0] in {1, self.cols_n-2} and move[1] in {1, self.rows_n-2}
        
        def getAgentMove(obs):
            possibleMoves = getValidMoves(obs)
            
            # Corner position first
            for move in possibleMoves:
                if isOnCorner(move):
                    return move
            
            # Side position next
            for move in possibleMoves:
                if isOnSide(move):
                    return move
            
            return possibleMoves[0]
        
        x, y = getAgentMove(obsNew)
        return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT
        