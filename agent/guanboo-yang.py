import pygame
from base_agent import BaseAgent, RandomAgent, HumanAgent

class MyAgent(BaseAgent):
    
    def __init__(self):
        super(MyAgent, self).__init__()
    
    def step(self, reward:dict, obs:dict) -> tuple:
        colorDict = {"black": -1, "white": 1, "empty": 0}
        colorNum = colorDict[self.color]
        
        def transfer(obsDict:dict) -> dict:
            '''
            obsDict: dict
                key: 0 ~ 63
                val: [-1, 0, 1]
            
            return : dict
                key: (x, y), where (7, 0) represents the top right
                val: [-1, 0, 1]
            '''
            return {(i % self.cols_n, i // self.cols_n):obsDict[i] for i in obsDict}
        
        obsNew=transfer(obs)    # new dictionary with 2D postion tuple keys
        
        def isOnBoard(self, x, y) -> bool:
            return 0 <= x < self.cols_n and 0 <= y < self.rows_n
        
        def isValidMove(self, move: tuple) -> list:
            if not self.isOnBoard(move[0], move[1]) or obs[(move[0], move[1])] != 0:
                return []
            obsNew[(move[0], move[1])] = colorNum
            # TODO: define another tile...
            dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            tilesToFlip = []
            for xdir, ydir in dirs:
                x, y = move[0]+xdir, move[1]+ydir
                while self.isOnBoard(x, y) and obsNew[(x, y)] == -colorNum:
                    x += xdir; y += ydir
                    if self.isOnBoard(x, y) and obsNew[(x, y)] == colorNum:
                        while True:
                            x -= xdir; y -= ydir
                            if x == move[0] and y == move[1]:
                                break
                            tilesToFlip.append((x, y))
            obsNew[(move[0], move[1])] = 0
            return tilesToFlip
        
        def getValidMoves(self, tile) -> list:
            return [[x, y] for x in range(self.cols_n) for y in range(self.rows_n) if self.isValidMove(tile, x, y)]