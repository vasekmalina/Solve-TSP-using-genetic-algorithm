import pygame
from pygame.locals import *
import numpy as np
import math
import copy as cp
import solve

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000,700
FPS = 60
RADIUS = 7.5
TSP_SOLVE_TIMES = 1

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
COLOR = (0,255,255)
GREEN = (124,252,0)
GRAY  = (105,105,105)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSP solving")
clock = pygame.time.Clock()

#func definition
def get_distant_matrix(points): 
    matrix = np.zeros((len(points), len(points)) , dtype='int16')
    matrix[0,2] = 5

    for index1, point1 in enumerate(points):
        for index2, point2 in enumerate(points):
            dis = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1])**2)
            dis = int(dis)
            matrix[index1, index2] = dis
    

    return matrix

def draw(points, count):
    screen.fill(BLACK)
    
    #drawing circles on position where mouse was clicked
    for point in points:
        pygame.draw.circle(screen, RED, point, RADIUS)


    #drawing line seperating draw window from  upper bar 
    pygame.draw.line(screen, WHITE,(0,20), (WIDTH, 20) ,1 )

    #init of notices in upper bar
    font = pygame.font.SysFont("comicsans", 25)
    text_distance = font.render("Distance: " + str(best_quality), 1, WHITE)
    text_start = font.render("SPACE to start", 1, WHITE)
    text_restart = font.render("R to restart", 1, WHITE)
    text_numbers = font.render("Q to switch on/off numbers", 1, WHITE)
    text_lines = font.render("W to switch on/off white lines", 1, WHITE)

    

    #drawing messages into upper bar
    SPACE = 10
    screen.blit(text_start, (0,0))
    screen.blit(text_restart, (text_start.get_width() + SPACE, 0))
    screen.blit(text_numbers, (text_start.get_width() + text_restart.get_width() + SPACE*2, 0))
    screen.blit(text_lines, (text_start.get_width() + text_restart.get_width() + 
                text_lines.get_width() + SPACE*3, 0))

    screen.blit(text_distance, (WIDTH - text_distance.get_width(),0))

    #print(WIDTH - text_distance.get_width() - text_count.get_width() - SPACE/2)

def draw_numbers(visible):
    if visible % 2 == 0:
        #drawing numbers below circles 
        for i in range(len(points)):
            circle_font = pygame.font.SysFont("comicsans", 25)
            circle_text = circle_font.render(str(i), 1, GREEN)
            pos = points[i]
            pos_x = pos[0] - circle_text.get_width()/2
            pos_y = pos[1] + circle_text.get_height()/2
            screen.blit(circle_text,(pos_x, pos_y))

#drawing all possible lines 
def draw_sec_lines(points, best_way, visible):
    if visible % 2 == 0:
        for index1 in best_way:
            for index2 in best_way:
                pygame.draw.line(screen, GRAY, points[index1],points[index2] ,1 )
        

#drawinng the best way calculated by algorithm
def draw_main_lines(points, best_way):
    #setup for drawing
    #for example:
    #[0,3,2,1] →

    #[0,3,2,1]
    #[3,2,1,0]
    bw1 = best_way.tolist()
    bw2 = cp.copy(bw1)
    item = bw2[0]
    bw2.remove(item)
    bw2.append(item)

    for i in range(len(bw1)):
        start = bw1[i]
        end = bw2[i]
        pygame.draw.line(screen, COLOR, points[start],points[end] ,5 )

    


points = []
running = True
start = False
best_way = []
best_quality = np.inf
allow = True
visible_lines = 0
visible_numbers = 0
count = 0
algo_condition_to_end = 25
space_clicked = 0 #variable which controls appending matrix to .txt file


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == MOUSEMOTION:
            pos = event.pos
            if pos[1] < 25:
                allow = False


        if event.type == MOUSEBUTTONDOWN and allow == True:
            points.append(event.pos)

        elif event.type == KEYDOWN:

            # User is allowed to press Space button multiple times,
            # because TSP algorithm usually does not find the best way on the first try 
            if event.key == K_SPACE and len(points) > 2:
                space_clicked += 1
                matrix = get_distant_matrix(points)

                while True:
                    bq, bw = solve.tsp_solve(matrix)
                    if bq < best_quality:   
                        best_quality = bq
                        best_way = bw
                        count = 0
                        #if the algorithm is not able to find better option "algo_condition_to_end" times then the algoritm ends.
                    if count == algo_condition_to_end:
                        count = 0
                        break
                    count += 1
                    print(count)


                start = True
                allow = False

            if event.key == K_r:
                start = False
                best_way = []
                best_quality = np.inf
                points.clear()
                allow = True
                count = 0
                space_clicked = 0

            if event.key == K_w:
                visible_lines += 1

            if event.key == K_q:
                visible_numbers += 1

          

    #drawing
    draw(points, count)
    if start:
        draw_main_lines(points, best_way)
        draw_sec_lines(points, best_way, visible_lines)
        draw_numbers(visible_numbers)

    pygame.display.update()
