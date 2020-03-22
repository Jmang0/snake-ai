from copy import deepcopy
import random
import math

class GameState:
    def __init__(self):
        self.snake = None
        self.direction =  None
        self.food = None
        self.dimensions = None

    def enter(self,snake,direction,food,dimensions):
        self.snake = snake
        self.direction = direction
        self.food = food
        self.dimensions = dimensions


gs = GameState()

def Move():
    head = gs.snake[0]
    if head[1] == gs.dimensions-2 and head[0] != 1:
        return [-1,0] #left
    
    if head[0] % 2 == 1:
        if head[1] != 1:
            return [0,-1] #up
        return [1,0] #right
    if head[1] == gs.dimensions-3 and head[0] != gs.dimensions-2:
        return [1,0] #right
    return [0,1] #down
