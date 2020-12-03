import pygame
from base_agent import BaseAgent, RandomAgent, HumanAgent


class MyAgent(BaseAgent):
    def __init__(self):
        super(MyAgent, self).__init__()
    
    def step(self, reward, obs):
        def transfer(obsDic):
            '''
            Transfer dictionary obsDic into a new dictionary which uses 2D position tuple as its keys instead of 1D index

            Return: a new dictionary with the modified key which in the form of (y,x)
                    where y indicates the col (from 0 to 7) and x represents the row (from 0 to 7)
            '''
            return {(i%self.cols_n,i//self.rows_n):obsDic[i] for i in obsDic}
        obsNew=transfer(obs)    #new dictionary with 2D postion tuple keys
