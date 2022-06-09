#### Imports ####
### import std lib
import copy
from math import floor, ceil, sqrt
import sys
import time
import random
### import external modules
import pygame
import pygame.freetype
from pygame.locals import *
from g_utils import *

class QixEnemy(object):
    def __init__(self, x, y, dx, dy, radius=25, color=(255, 255, 0)):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.radius = radius
        self.color = color

    def move(self, dt, game_board, game_states, config):
        
        lc = 0;
        rc = 0;
        tc = 0;
        bc = 0;
        l_dir, r_dir, t_dir, b_dir = self.wallCollision(game_board.game_matrix)

        playerCollision = foundQIX(config['player'].player_coords['x'], config['player'].player_coords['y'], self.x, self.y, self.radius, 15);
        potential_wall_collision = False
        for wall in game_board.potentialWalls:
            if foundQIX(wall[0], wall[1], self.x, self.y, self.radius, 15):
                potential_wall_collision = True
                break;


        if playerCollision or potential_wall_collision:
            game_states['insideGame']['lives'] = game_states['insideGame']['lives'] - 1
            config['player'].player_coords['x'] = 0
            config['player'].player_coords['y'] = 0
            game_board.potentialWalls = {}
            game_states['insideGame']['tryingToCapture'] = False

        elif (l_dir or r_dir or t_dir or b_dir):
            print('hitting wall');
            # time.sleep(1)
            if l_dir:
                # print('here 11111111111111111:', random.uniform(5, 10))
                lc = lc + 1;
                self.dx = -abs(self.dx)
                tempDx = self.dx - random.uniform(5, 10)
                self.x += tempDx
                # self.y = ceil(self.y);
                self.y += self.dy * dt

                # if (lc >= 10):
                #     self.x += self.dx - random.uniform(0.2, 0.5)
                #     lc = 0;

            if r_dir:
                rc = rc + 1;
                self.dx = abs(self.dx)
                tempDx = self.dx + random.uniform(5, 10)
                self.x += tempDx
                # self.y = floor(self.y);
                self.y += self.dy * dt

                # special edge cases
                # if (rc >= 10):
                #     print('here 2', l_dir, r_dir, t_dir, b_dir);
                #     self.x += self.dx + random.uniform(0.2, 0.5)
                #     rc = 0;
                # elif (rc >= 3 and bc >= 3):
                #     self.x += 10

            
            if t_dir:
                tc = tc + 1;
                self.dy = abs(self.dy)
                tempDy = self.dy + random.uniform(5, 10)
                self.y += tempDy
                # self.x = floor(self.x);
                self.x += self.dx * dt

                # if (tc >= 10):
                #     self.y += self.dy + random.uniform(0.5, 0.7)
                #     tc = 0;

            if b_dir:
                bc = bc + 1;
                self.dy = - abs(self.dy)
                tempDy = self.dy - random.uniform(5, 10)
                self.y += tempDy
                # self.x = ceil(self.x);
                self.x += self.dx * dt

                # if (bc >= 10):
                #     self.y += self.dy - random.uniform(0.5, 0.7)
                #     bc = 0;

        else:
            lc = 0;
            rc = 0;
            tc = 0;
            bc = 0;
            # print('normal move')
            self.x += self.dx * dt
            self.y += self.dy * dt



        ############# game area bounds checks, only needed for precaution
        # check if out of bounds in x axis
        if self.x <= 0:
            self.dx = abs(self.dx)
            self.x += self.dx
        elif self.x >= config['width']:
            self.dx = -abs(self.dx)
            self.x += self.dx
        
        # check if out of bounds in y axis
        if self.y <= 0:
            self.dy = abs(self.dy)
            self.y += self.dy
        elif self.y >= config['height']:
            self.dy = -abs(self.dy)
            self.y += self.dy

    
    def wallCollision(self, gameMatrix):
        
        l_dir, r_dir, t_dir, b_dir = False, False, False, False
        intersect = False

        for row in range(0, len(gameMatrix)):
            if not intersect:
                for col in range(0, len(gameMatrix[row])):
                    if gameMatrix[row][col]['w'] == True:
                        l_dir, r_dir, t_dir, b_dir = False, False, False, False
                        intersect = self.circleIntersection(self.x, self.y, gameMatrix[row][col]['x'] + 25, gameMatrix[row][col]['y'] + 25, self.radius, 25);
                        if intersect:
                            print('intersect')

                            if abs(self.y - gameMatrix[row][col]['y']) <= abs(self.x - gameMatrix[row][col]['x']):
                                if gameMatrix[row][col]['y'] + 25 >= self.y:
                                    b_dir = True
                                    # check left
                                    print('ball hit bottom side of wall')
                                    if self.matrixCoordIsValid(row + 1, col - 1, gameMatrix):
                                        if gameMatrix[row + 1][col - 1]['x'] + 25 >= self.x:
                                            l_dir = True
                                    # check right intersect
                                    elif self.matrixCoordIsValid(row + 1, col + 1, gameMatrix):
                                        if gameMatrix[row + 1][col + 1]['x'] + 25 <= self.x:
                                            r_dir = True
                                    break
                                # bot intersect
                                elif gameMatrix[row][col]['y'] + 25 <= self.y:
                                    t_dir = True
                                    # check left
                                    print('ball hit top side of wall')
                                    if self.matrixCoordIsValid(row - 1, col - 1, gameMatrix):
                                        if gameMatrix[row - 1][col - 1]['x'] + 25 >= self.x:
                                            l_dir = True
                                    # check right intersect
                                    elif self.matrixCoordIsValid(row - 1, col + 1, gameMatrix):
                                        if gameMatrix[row - 1][col + 1]['x'] + 25 <= self.x:
                                            r_dir = True
                                    break
                            else:
                                # left intersect
                                if gameMatrix[row][col]['x'] + 25 >= self.x:
                                    l_dir = True
                                    print('ball hit left side of wall')
                                    # check top
                                    if self.matrixCoordIsValid(row - 1, col + 1, gameMatrix):
                                        if gameMatrix[row - 1][col + 1]['y'] + 25 >= self.y:
                                            t_dir = True
                                    # check bot intersect
                                    elif self.matrixCoordIsValid(row + 1, col + 1, gameMatrix):
                                        if gameMatrix[row + 1][col + 1]['y'] + 25 <= self.y:
                                            b_dir = True
                                    break;
                                # right intersect
                                elif gameMatrix[row][col]['x'] + 25 <= self.x:
                                    r_dir = True
                                    print('ball hit right side of wall')
                                    # check top
                                    if self.matrixCoordIsValid(row - 1, col - 1, gameMatrix):
                                        if gameMatrix[row - 1][col - 1]['y'] + 25 >= self.y:
                                            t_dir = True
                                    # check bot intersect
                                    elif self.matrixCoordIsValid(row + 1, col - 1, gameMatrix):
                                        if gameMatrix[row + 1][col - 1]['y'] + 25 <= self.y:
                                            b_dir = True
                                    break;



        return (l_dir, r_dir, t_dir, b_dir)

    def circleIntersection(self, c1x, c1y, c2x, c2y, r1, r2):
        distanceBetweenC1C2 = sqrt(pow((c1x - c2x), 2) + pow((c1y - c2y), 2))
        if distanceBetweenC1C2 <= r1 + r2:
            return True
        else:
            return False

    def matrixCoordIsValid(self, row, col, game_matrix):
        rowValid = False
        colValid = False
        if 0 <= row and row < len(game_matrix):
            rowValid = True
        if 0 <= col and col < len(game_matrix[0]):
            colValid = True

        return rowValid and colValid

    def render(self, screen):
        # print(self.radius,  self.color, (floor(self.x), floor(self.y), self.radius)
        pygame.draw.circle(screen, self.color, (floor(self.x), floor(self.y)), self.radius)
