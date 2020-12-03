import pygame
from base_agent import BaseAgent, RandomAgent, HumanAgent


class MyAgent(BaseAgent):
    def __init__(self):
        super(MyAgent, self).__init__()
    
    def step(self, reward, obs): # assume we are 1
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


test = MyAgent()
test.step(0, {0: 1, 1: 1})