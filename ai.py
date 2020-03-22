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

def evalMove(in_snake,moves):
    snake = deepcopy(in_snake)
    #Get the position of the new snake
     # move the list over one
    
    for move in moves:
        snake[1:] = deepcopy(snake)[:-1]
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
        score -= 1000000

    #Check if eaten food
    if head == gs.food:
        score += 500000


    #Adjust score depending on distance from food
    score -= math.sqrt((gs.food[0]-head[0])**2 + (gs.food[1]-head[1])**2)
    #bodyavg = [int(sum([i[n] for i in gs.snake])/len(gs.snake)) for n in [0,1]]
    #score += int(pos(bodyavg[0]-head[0]) + pos(bodyavg[1]-head[1]))/2
    #print("---Move:",move)
    #print("Head pos:",head)
    #print("Avg body pos:",bodyavg)
    
    bodycount = 0
    for x in range(-3,4):
        for y in range(-3,4):
            square = [head[0]+x,head[1]+y]
            valid = True
            for n in [0,1]:
                if square[n] < 0 or square[n] > gs.dimensions-1:
                    valid = False
            if valid:
                if square in snake:
                    score -= 1
    return score



def tree(move,depth,lst=[],scores=[]):
    if depth == 0:
        global data
        data.append([sum(deepcopy(scores)),deepcopy(lst)])
    else:
        for move in choices(move):
            lst.append(move)
            scores.append(evalMove(gs.snake,lst))
            tree(move,depth-1,lst,scores)
            lst.pop(len(lst)-1)
            scores.pop(len(scores)-1)

data = []
def Move(search_depth=2):
    global data

    data = []
    #print("----------------")
    #print("Current Direction:",gs.direction)

    #Gets all possible moves int data
    tree(gs.direction,search_depth)

    # print(evalMove(gs.snake,[gs.direction]))
    # print(evalMove(gs.snake,[gs.direction for i in range(20)])

    scores = [i[0] for i in data]
    best = []
    for n in range(len(data)):
        if scores[n] == max(scores):
            best.append(data[n][1])
     
    if best[0][0] == [i/-1 for i in gs.direction]:
        print("--------------------------------")
        for i in data:
            print(i)
        print("Best:")
        for i in best:
            print(i)
        print("Current Direction:")
        print(gs.direction)
    
    return best[0][0]
