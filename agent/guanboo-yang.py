import pygame
from base_agent import BaseAgent, RandomAgent, HumanAgent


class MyAgent(BaseAgent):
    
    def __init__(self):
        super(MyAgent, self).__init__()
    
    def step(self, reward:dict, obs:  dict) -> tuple:  # assume we are 1
        def transfer(obsDic:dict) -> dict:
            '''
            Transfer dictionary obsDic into a new dictionary which uses 2D position tuple as its keys instead of 1D index

            Return: Dictionary. A new dictionary with the modified key which in the form of (y,x)
            where y indicates the col (from 0 to 7) and x represents the row (from 0 to 7)
            '''
            return {(i%self.cols_n,i//self.rows_n):obsDic[i] for i in obsDic}
        obsNew=transfer(obs)    #new dictionary with 2D postion tuple keys
        
        def change(num):
            return num // self.cols_n, num % self.cols_n
        
        def isOnBoard(self, x, y):
            return 0 <= x < self.cols_n and 0 <= y < self.rows_n
        
        def isValidMove(self, move: tuple) -> list:
            if not self.isOnBoard(move[0], move[1]) or obs[(move[0], move[1])] != 0:
                return []
            obs[(move[0], move[1])] = 1
            # TODO: define another tile...
            dirs = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            tilesToFlip = []
            for xdir, ydir in dirs:
                x, y = move[0]+xdir, move[1]+ydir
                while self.isOnBoard(x, y) and obs[(x, y)] == -1:
                    x += xdir; y += ydir
                    if self.isOnBoard(x, y) and obs[(x, y)] == 1:
                        while True:
                            x -= xdir; y -= ydir
                            if x == move[0] and y == move[1]:
                                break
                            tilesToFlip.append((x, y))
            obs[(move[0], move[1])] = 0
            return tilesToFlip
