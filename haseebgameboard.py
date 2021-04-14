from collections import deque
from math import floor
import pygame

class GameBoard(object):
    
    def __init__(self, board_config):
        self.wallsInPlace = {}
        self.potentialWalls = {}
        self.height = board_config['screen_height']
        self.width = board_config['screen_width']
        self.wall_size = board_config['wall_size']
        self.qixEnemy = board_config['enemy']

        self.game_matrix = []

        self.generate_game_matrix()
        self.generate_initial_walls()
        self.syncMatrixWithWalls()

    def generate_initial_walls(self):
        for w in range(0, self.width, self.wall_size):
            xCoord = w
            yCoord = 0
            self.wallsInPlace[(xCoord, yCoord)] = True

        for w in range(0, self.width, self.wall_size):
            xCoord = w
            yCoord = self.height - self.wall_size
            self.wallsInPlace[(xCoord, yCoord)] = True

        for h in range(0, self.height, self.wall_size):
            xCoord = 0
            yCoord = h
            self.wallsInPlace[(xCoord, yCoord)] = True

        for h in range(0, self.height, self.wall_size):
            xCoord = self.width - self.wall_size
            yCoord = h
            self.wallsInPlace[(xCoord, yCoord)] = True

    def generate_game_matrix(self):
        for row in range(0, self.height, self.wall_size):
            
            newRow = []
            
            for col in range(0, self.width, self.wall_size):
                newRow.append({'x': col, 'y': row, 'w': False, 'f': False})
            
            self.game_matrix.append(newRow)

    def syncMatrixWithWalls(self):
        for wall in self.wallsInPlace:
            row = floor(wall[0]/self.wall_size)
            col = floor(wall[1]/self.wall_size)
            self.game_matrix[col][row]['w'] = True
            self.game_matrix[col][row]['f'] = True

    def render(self, screen):
        for row in self.game_matrix:
            for tile in row:
                if tile['w'] == True:
                    pygame.draw.rect(screen, (0, 80, 230), [tile['x'], tile['y'], self.wall_size, self.wall_size], 0)

        for wall in self.potentialWalls:
            pygame.draw.rect(screen, (227, 10, 140), [wall[0], wall[1], self.wall_size, self.wall_size], 0)





    


    def matrixCapture(self):
        frontier_1 = deque()
        visited_1 = {}
        capture_area = [1, 1]
        frontier_1.popleft
        # find target to start flood fill
        flood_target_1 = self.findFloodingTarget()
        # then run flood fill to check if area is capturable
        flood_result_1 = None
        if flood_target_1 != None:
            flood_result_1 = self.floodFill_breathFirstSearch(frontier_1, visited_1, flood_target_1['x'], flood_target_1['y'], self.enemyInfo['x'], self.enemyInfo['y'])
    #     # run flood fill
    #     # if no enemy encountered, capture area
    #     # if enemy encountered, run flood fill again and capture other area
    #     # win game once captured 65% of area
    #     # keep in mind edge case when capturing a 0 width rectangle, thus flood fill 1 and 2 will fail, 