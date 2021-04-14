import pygame
from g_utils import *
from collections import deque

from math import floor

class Player(object):
    def __init__(self, player_color=(227, 216, 0), player_size=50):
        self.player_color = player_color
        self.player_color_flag = [0]
        self.player_size = player_size
        self.filled = 0
        self.player_coords = { 'x': 0, 'y': 0}

    # def get_color_flag(self):
    #     return self.player_color_flag[0]

    def flip_color_flag(self, flashColor):
        if self.player_color_flag[0] == 0:
            self.player_color_flag[0] = 1
            return self.player_color
        else:
            self.player_color_flag[0] = 0
            return flashColor

    def move_player(self, direction, game_states, game_board):
        newX = self.player_coords['x']
        newY = self.player_coords['y']
        if direction == 'left':
            newX = self.player_coords['x'] - self.player_size
        elif direction == 'right':
            newX = self.player_coords['x'] + self.player_size
        elif direction == 'up':
            newY = self.player_coords['y'] - self.player_size
        elif direction == 'down':
            newY = self.player_coords['y'] + self.player_size
       
        if not game_states['insideGame']['tryingToCapture']:
            if direction == 'left' or direction == 'right':
                self.player_coords['x'] = newX
            else:
                self.player_coords['y'] = newY
            if (newX, newY) not in game_board.wallsInPlace:
                game_states['insideGame']['tryingToCapture'] = True
                game_board.potentialWalls = {}
                game_board.potentialWalls[(newX, newY)] = True
        else:
            # successful capture: safe
            if (newX, newY) in game_board.wallsInPlace and (newX, newY) not in game_board.potentialWalls:
                game_states['insideGame']['tryingToCapture'] = False
                game_board.wallsInPlace.update(game_board.potentialWalls)
                ##### Flood Fill #####
                # divide matrix into two areas
                game_board.syncMatrixWithWalls()
                # run flood fill on both areas
                ft = findFloodingTarget(game_board.game_matrix)
                ## flood target is in pixel coords which have to be turned back into matrix indexes
                if ft != None:
                    frontier = deque()
                    visited = {}
                    enemyConfig = {
                        'x': floor(game_board.qixEnemy.x/50),
                        'y': floor(game_board.qixEnemy.y/50),
                        'radius': game_board.qixEnemy.radius,
                        'ax': game_board.qixEnemy.x,
                        'ay': game_board.qixEnemy.y,
                        'enemyFound': False
                    }
                    gameConfig = {
                        'width': game_board.width, 'height': game_board.height, 'wall_size': self.player_size
                    }
                    floodFill_breathFirstSearch(gameConfig, game_board.game_matrix, frontier, visited, floor(ft['x']/50), floor(ft['y']/50), enemyConfig)

                    # if we didn't encounter any enemies capture the given area else mark it as flooded
                    if enemyConfig['enemyFound'] == False:
                        # print('didnt find in left side')
                        for tile in visited:
                            game_board.game_matrix[tile[1]][tile[0]]['w'] = True
                    else:
                        for tile in visited:
                            game_board.game_matrix[tile[1]][tile[0]]['f'] = True
                

                    # no enemy on left side
                    if enemyConfig['enemyFound']:
                        ft2 = findFloodingTarget(game_board.game_matrix)
                        if ft2 != None:
                            # print('flood target 1', ft2)
                            frontier = deque()
                            visited = {}
                            enemyConfig2 = {
                                'x': floor(game_board.qixEnemy.x/50),
                                'y': floor(game_board.qixEnemy.y/50),
                                'radius': game_board.qixEnemy.radius,
                                'ax': game_board.qixEnemy.x,
                                'ay': game_board.qixEnemy.y,
                                'enemyFound': False
                            }
                            gameConfig = {
                                'width': game_board.width, 'height': game_board.height, 'wall_size': self.player_size
                            }
                            floodFill_breathFirstSearch(gameConfig, game_board.game_matrix, frontier, visited, floor(ft2['x']/50), floor(ft2['y']/50), enemyConfig2)
                                            # if we didn't encounter any enemies capture the given area else mark it as flooded
                            if enemyConfig2['enemyFound'] == False:
                                # print('didnt find in right side')
                                for tile in visited:
                                    game_board.game_matrix[tile[1]][tile[0]]['w'] = True
                            else:
                                for tile in visited:
                                    game_board.game_matrix[tile[1]][tile[0]]['f'] = True
                
                # reset flooded tiles to avoid bugs
                for row in game_board.game_matrix:
                    for tile in row:
                        if tile['w'] == False:
                            tile['f'] = False
                game_board.potentialWalls = {}

                ########################### may not needed

                # game_board.wallsInPlace = {}

                ##############################################

                numTiles = 0
                WallTiles = 0
                for row in game_board.game_matrix:
                    for tile in row:
                        numTiles = numTiles + 1
                        if tile['w'] == True:
                            WallTiles = WallTiles + 1
                            game_board.wallsInPlace[(tile['x'], tile['y'])] = True
                
                game_states['insideGame']['area'] = (WallTiles/numTiles)*100
                # print(f'============= area captured {(WallTiles/numTiles)*100} ================= {WallTiles}/{numTiles}')
                if direction == 'left' or direction == 'right':
                    self.player_coords['x'] = newX
                else:
                    self.player_coords['y'] = newY
            # in process of capturing: unsafe
            elif (newX, newY) not in game_board.wallsInPlace and (newX, newY) not in game_board.potentialWalls:
                # qix collision
                if foundQIX(self.player_coords['x'] + 25, self.player_coords['y'] + 25, game_board.qixEnemy.x, game_board.qixEnemy.y, game_board.qixEnemy.radius, 15):
                    print('ouch')
                    game_states['insideGame']['lives'] = game_states['insideGame']['lives'] - 1
                    self.player_coords['x'] = 0
                    self.player_coords['y'] = 0
                    game_board.potentialWalls = {}
                    game_states['insideGame']['tryingToCapture'] = False
                else:
                    if direction == 'left' or direction == 'right':
                        self.player_coords['x'] = newX
                    else:
                        self.player_coords['y'] = newY
                    game_board.potentialWalls[(newX, newY)] = True

    def render(self, screen, gameState):
        if gameState:
            pygame.draw.rect(screen, self.flip_color_flag((227, 10, 140)), [self.player_coords.get('x'), self.player_coords.get('y'), self.player_size, self.player_size], self.filled)
        else:
            pygame.draw.rect(screen, self.flip_color_flag((0, 80, 230)), [self.player_coords.get('x'), self.player_coords.get('y'), self.player_size, self.player_size], self.filled)