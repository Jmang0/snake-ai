import pygame, sys
import pygame.freetype
from random import randint
from copy import deepcopy
from time import time, sleep
import ai as ai

pygame.init()

squareSize = 20
dimensions = 20
screenSize = int(squareSize*dimensions)

screen = pygame.display.set_mode((screenSize,screenSize+70))
pygame.display.set_caption("Snake")
scoreText= pygame.freetype.Font(None, 25)

WHITE = pygame.Color(255,255,255)
BLACK = pygame.Color(0,0,0)
RED = pygame.Color(255,0,0)
WALLCOLOUR = pygame.Color(0, 0, 130)

#Define functions
def drawRect(point,colour):
    rect = pygame.Rect(point[0]*squareSize+1,point[1]*squareSize+1,squareSize-2,squareSize-2)
    pygame.draw.rect(screen,colour,rect)


#Initialize game variables
snake = [[1,9]]
direction = [1,0]
food = [randint(1,dimensions-2),randint(1,dimensions-2)]
dead = False
frame = 0
score = 0

limit_fps = False
fps = 30
frameTime = 1/fps

auto = True

try:
    highscore = int(open("highscore.txt","r").readline())
except ValueError:
    highscore = 0
state = "game"
score_record = []

while state != "end":
    if state == "game":
        startTime = time()
        frame += 1
        keydown = False
        dirtyRects = []
        #----- Event Handling -----
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Closing the program
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not auto:
                if not keydown:
                    keydown = True
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        if direction != [0,1]:
                            direction = [0,-1]
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if direction != [0,-1]:
                            direction = [0,1]
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if direction != [1,0]:
                            direction = [-1,0]
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if direction != [-1,0]:
                            direction = [1,0]
                    else:
                        keydown = False

        #----- AI code here -----
        if auto:
            ai.gs.enter(snake,direction,food,dimensions)
            direction = ai.Move()

        #----- Update game state -----
        drawRect(snake[-1],BLACK) #Draw the end of the snake black

        #Move snake
        snake[1:] = deepcopy(snake[:-1]) # move the list over one
        for n in [0,1]:
            snake[0][n] += direction[n] #replace the first one


        #Snake collisions
        head = snake[0]
        if snake.count(head) > 1: #check if the snake is moving into itself
            dead = True
        if head == food:
            score += 1
            snake.append([snake[-1][n]-direction[n] for n in [0,1]])
            while food in snake:
                food = [randint(1,dimensions-2),randint(1,dimensions-2)]
        for n in [0,1]: #Wall collisions
            if head[n] == 0 or head[n] == dimensions-1:
                dead = True
        if dead:
            print("Score:",score)
            if score > highscore:
                f = open("highscore.txt","w")
                f.write(str(score))
                highscore = score
            state = "gameover"
        else:
            #----- Drawing to screen -----
            #Walls
            screen.fill((0,0,0))
            for x in range(dimensions):
                for y in range(dimensions):
                    for axis in [x,y]: #Wall collisions
                        if axis == 0 or axis == dimensions-1:
                            pygame.draw.rect(screen,WALLCOLOUR,
                                             (x*squareSize,y*squareSize,
                                              squareSize,squareSize))
            #Food
            drawRect(food,RED)
            #Snake
            for point in snake:
                drawRect(point,WHITE)
            #Text
            scoreText.render_to(screen, (40,screenSize+25), "Score: "+str(score), (255,255,255)) # display score
            scoreText.render_to(screen, (screenSize/2,screenSize+25), "Highscore: "+str(highscore), (255,255,255)) # display score

            #Time
            if limit_fps:
                timeTaken = time()-startTime
                if timeTaken < frameTime:
                    sleep(frameTime-timeTaken)

            #Draw to screen
            pygame.display.flip()

    elif state == "gameover":
        restart = False
        score_record.append(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Closing the program
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                restart = True
        if restart or auto:
            #Initialize game variables:
            snake = [[3,9]]
            direction = [1,0]
            food = [randint(1,dimensions-2),randint(1,dimensions-2)]
            dead = False
            frame = 0
            score = 0
            state = "game"


        scoreText.render_to(screen, (screenSize/2-75,screenSize/2-25), "GAME OVER", (255,0,0)) # display score
        pygame.display.update()
