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

def pos(n):
    if n > 0:
        return n
    return -n

def choices(x):
    directions = [[1,0],[-1,0],[0,1],[0,-1]]
    directions.remove([i/-1 for i in x])
    return directions

def eval(snake,move):
    snake = deepcopy(snake)
    #Get the position of the new snake
    snake[1:] = deepcopy(snake)[:-1] # move the list over one
    for n in [0,1]:
        snake[0][n] += move[n] #replace the first one

    #Evaluate score of new position
    score = 0

    #Check if dead
    dead = False
    head = snake[0]
    if snake.count(head) > 1: #check if the snake is moving into itself
        dead = True
    for n in [0,1]: #Wall collisions
        if head[n] == 0 or head[n] == gs.dimensions-1:
            dead = True
    if dead:
        score -= 10000

    #Check if eaten food
    if head == gs.food:
        score += 5000
    else:
        #Adjust score depending on distance from food
        distance = math.sqrt((gs.food[0]-head[0])**2 + pos(gs.food[1]-head[1])**2)
        score -= distance
    
        #print(score)
        #bodyavg = [int(sum([i[n] for i in gs.snake])/len(gs.snake)) for n in [0,1]]
    #score += int(pos(bodyavg[0]-head[0]) + pos(bodyavg[1]-head[1]))/2
    #print("---Move:",move)
    #print("Head pos:",head)
    #print("Avg body pos:",bodyavg)
##    bodycount = 0
##    for x in range(-3,4):
##        for y in range(-3,4):
##            square = [head[0]+x,head[1]+y]
##            valid = True
##            for n in [0,1]: #Wall collisions
##                if square[n] < 0 or square[n] > gs.dimensions-1:
##                    valid = False
##            if valid:
##                if square in snake:
##                    score -= 1
##                else:
##                    score += 1

    return score

def Move():
    #print("Average x of snake:",sum([i[0] for i in gs.snake])/len(gs.snake))

    data = []
    for move in choices(gs.direction):
        data.append([move,eval(gs.snake,move)])

    scores = [i[1] for i in data]
    best = []
    for n in range(3):
        if data[n][1] == max(scores):
            best.append(data[n][0])

    return random.choice(best)
