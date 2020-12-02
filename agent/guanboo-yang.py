import pygame
from base_agent import BaseAgent, RandomAgent, HumanAgent


class MyAgent(BaseAgent):
    def __init__(self):
        super(MyAgent, self).__init__()
    
    def step(self, reward, obs):
        def change(num):
            return num // self.cols_n, num % self.cols_n


test = MyAgent()
test.step(0, {0: 1, 1: 1})