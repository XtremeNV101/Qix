#### Imports ####
### import std lib
import copy
from math import floor
import sys
### import external modules
import pygame
import pygame.freetype
from pygame.locals import *
#### import internal modules
from gameboard import GameBoard
from menu import Menu
from player import Player
from enemy import QixEnemy
from wall import Wall
from g_utils import *
from enemies import Enemy
# initialize all pygame modules
pygame.init()
GAME_FONT = pygame.freetype.Font("ka1.ttf", 24)
heart = pygame.image.load('heart.jpg')
#### Set up data ####
screen_width = 1000
screen_height = 600
screen_background_color = (255, 255, 255)
block_size = 50

game_board_width = screen_width
game_board_height = screen_height - 100

#### game_states ####
game_states = {
    'running': True,
    'outsideGame': False,
    'insideGame': { # in menu or in game
        'tryingToCapture': False,
        'lives': 3,
        'area': 0
    },
    'wonRound': False,
    'startedOnce': False
}

#### Main enemy ####
enemy_size = block_size
enemy_x = game_board_width - enemy_size - block_size*5
enemy_y = game_board_height - 100 - enemy_size - block_size*2
enemy_speed = 2

#### Game Objects ####
mainPlayer = Player()

game_menu = Menu({
    'screen_width': screen_width,
    'screen_height': screen_height
})

# qixEnemy = QixEnemy(enemy_x, enemy_y, 2, 2, 20, (139, 0, 139))
# qixEnemy = QixEnemy(enemy_x, enemy_y, 4, 4, 25, (139, 0, 139))
qixEnemy = QixEnemy(enemy_x, enemy_y, enemy_speed, enemy_speed, 25, (139, 0, 139))
###spark
enemyOne =  Enemy(450, 0)
###sparkTwo
enemyTwo = Enemy(450, 0)
game_board = GameBoard({
    'screen_width': game_board_width,
    'screen_height': game_board_height,
    'wall_size': block_size,
    'enemy': qixEnemy
})

# set up drawing window
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()
leftist = True
ups = True
lefts = True
upsa = True
blank = True
blanks = True
while game_states['running']:
    dt = clock.tick(24)
    if game_states['outsideGame']:
        #### React to events ####
        ###enemyOne
        ##enemy 1
        if blank == True:
            if enemyOne.x <= 0:
                enemyOne.x = 0
                enemyOne.y += 7
            elif enemyOne.x >= 950:
                enemyOne.x = 950
                enemyOne.y -= 7
            
            if enemyOne.y <= 0:
                enemyOne.y = 0
                enemyOne.x -= 7
            elif enemyOne.y >= 450:
                enemyOne.y = 450
                enemyOne.x += 7    
        ###enemyTwo

        if blanks == True:
            if enemyTwo.x <= 0:
                enemyTwo.x = 0
                enemyTwo.y -= 7
            elif enemyTwo.x >= 950:
                enemyTwo.x = 950
                enemyTwo.y += 7
            
            if enemyTwo.y <= 0:
                enemyTwo.y = 0
                enemyTwo.x += 7
            elif enemyTwo.y >= 450:
                enemyTwo.y = 450
                enemyTwo.x -= 7   

        ### Check keyboard events
        for event in pygame.event.get():
            if event.type == QUIT:
                game_states['running'] = False
            
            # handle keyboard input
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_LEFT]:
                if mainPlayer.player_coords['x'] >= mainPlayer.player_size:
                    mainPlayer.move_player('left', game_states, game_board)
            elif pressed_keys[K_RIGHT]:
                if mainPlayer.player_coords['x'] <= game_board_width - mainPlayer.player_size*2:
                    mainPlayer.move_player('right', game_states, game_board)
            elif pressed_keys[K_UP]:
                if mainPlayer.player_coords['y'] >= mainPlayer.player_size:
                    mainPlayer.move_player('up', game_states, game_board)
            elif pressed_keys[K_DOWN]:
                if mainPlayer.player_coords['y'] <= game_board_height - mainPlayer.player_size*2:
                    mainPlayer.move_player('down', game_states, game_board)
        if game_states['insideGame']['tryingToCapture']:
            speed = 5
            enemyOne.move(speed, mainPlayer.player_coords['x'],mainPlayer.player_coords['y'])
            if (enemyOne.x <= mainPlayer.player_coords['x'] and enemyOne.x >= mainPlayer.player_coords['x'] - speed) or (enemyOne.x >= mainPlayer.player_coords['x'] and enemyOne.x <= mainPlayer.player_coords['x'] + speed):
                    enemyOne.x = mainPlayer.player_coords['x']
            if (enemyOne.y <= mainPlayer.player_coords['y'] and enemyOne.y >= mainPlayer.player_coords['y'] - speed) or (enemyOne.y >= mainPlayer.player_coords['y'] and enemyOne.y <= mainPlayer.player_coords['y'] + speed):
                enemyOne.y = mainPlayer.player_coords['y']
            enemyTwo.move(speed, mainPlayer.player_coords['x'],mainPlayer.player_coords['y'])
            if (enemyTwo.x <= mainPlayer.player_coords['x'] and enemyTwo.x >= mainPlayer.player_coords['x']) or (enemyTwo.x >= mainPlayer.player_coords['x'] and enemyTwo.x <= mainPlayer.player_coords['x']):
                    enemyTwo.x = mainPlayer.player_coords['x']
            if (enemyTwo.y <= mainPlayer.player_coords['y'] and enemyTwo.y >= mainPlayer.player_coords['y']) or (enemyTwo.y >= mainPlayer.player_coords['y'] and enemyTwo.y <= mainPlayer.player_coords['y']):
                enemyTwo.y = 450
            blank = False
            blanks = False
        elif blank == False or blanks == False:
            if blank == False:
                speed = 5
                enemyOne.move(speed, 450,0)
                if (enemyOne.x <= 450 and enemyOne.x >= 450 - speed) or (enemyOne.x >= 450 and enemyOne.x <= 450 + speed):
                    enemyOne.x = 450
                if (enemyOne.y <= 0 and enemyOne.y >= 0 - speed) or (enemyOne.y >= 0 and enemyOne.y <= 0 + speed):
                    enemyOne.y = 0
                if (enemyOne.x == 450 and enemyOne.y == 0) or enemyOne.y == 0:
                    blank = True
            if blanks == False:
                speed = 5
                enemyTwo.move(speed, 950,450)
                if (enemyTwo.x <= 950 and enemyTwo.x >= 950 - speed) or (enemyTwo.x >= 950 and enemyTwo.x <= 950 + speed):
                    enemyTwo.x = 950
                if (enemyTwo.y <= 450 and enemyTwo.y >= 450 - speed) or (enemyTwo.y >= 450 and enemyTwo.y <= 450 + speed):
                    enemyTwo.y = 450
                if (enemyTwo.x == 950 and enemyTwo.y == 450) or enemyTwo.y == 450:
                    blanks = True
        if game_states['insideGame']['lives'] > 0 and game_states['insideGame']['area'] <= 80:
            #### Do Calculations
            percentDT = dt/(24)
            qixEnemy.move(percentDT, game_board, game_states, {
                'width': game_board_width,
                'height': game_board_height,
                'player': mainPlayer
            })
            
            #### Render game objects ####
            ### Reset screen
            screen.fill(screen_background_color)
            
            ### Render walls
            game_board.render(screen)
            
            ### Render player
            mainPlayer.render(screen, game_states['insideGame']['tryingToCapture'])
            playerRect = pygame.Rect(mainPlayer.player_coords['x'], mainPlayer.player_coords['y'], 50, 50)
            ### Render main enemy
            # pygame.draw.rect(screen, (10, 220, 30), [300, 300, enemy_size, enemy_size], 0)

            ### render moving qix enemy
            qixEnemy.render(screen)
            ### sparks
            enemyOneRect = pygame.Rect(enemyOne.x, enemyOne.y, 50, 50)
            enemyTwoRect = pygame.Rect(enemyTwo.x, enemyTwo.y, 50, 50)
            pygame.draw.rect(screen, (100, 100, 100), enemyOneRect, 0)
            pygame.draw.rect(screen, (255, 0, 255), enemyTwoRect, 0)
            ###collision with qix when player is not moving
            if foundQIX(mainPlayer.player_coords['x'] + 25, mainPlayer.player_coords['y'] + 25, game_board.qixEnemy.x, game_board.qixEnemy.y, game_board.qixEnemy.radius, 15):
                game_states['insideGame']['lives'] = game_states['insideGame']['lives'] - 1
                mainPlayer.player_coords['x'] = 0
                mainPlayer.player_coords['y'] = 0
                game_board.potentialWalls = {}
                game_states['insideGame']['tryingToCapture'] = False
            ###collision with sparks
            naruto = True
            for wall in game_board.potentialWalls:
                little = pygame.Rect(wall[0], wall[1], game_board.wall_size, game_board.wall_size)
                if little.colliderect(enemyTwoRect):
                    naruto = False
                if little.colliderect(enemyOneRect):
                    naruto = False
            if playerRect.colliderect(enemyTwoRect) and naruto == True:
            #if foundQIX(floor(mainPlayer.player_coords['x']/50), floor(mainPlayer.player_coords['y']/50), floor(game_board.enemyInfo['x']/50), floor(game_board.enemyInfo['y']/50)):
                game_states['insideGame']['lives'] = game_states['insideGame']['lives'] - 1
                mainPlayer.player_coords['x'] = 0
                mainPlayer.player_coords['y'] = 0
                if abs(enemyTwo.x - mainPlayer.player_coords['x']) <= 45 and abs(enemyTwo.y - mainPlayer.player_coords['x']) <= 45:
                    mainPlayer.player_coords['x'] = 950
                    mainPlayer.player_coords['y'] = 450
                game_board.potentialWalls = {}
                game_states['insideGame']['tryingToCapture'] = False
                mainPlayer.render(screen, game_states['insideGame']['tryingToCapture'])
            elif naruto == False:
                game_states['insideGame']['lives'] = game_states['insideGame']['lives'] - 1
                mainPlayer.player_coords['x'] = 0
                mainPlayer.player_coords['y'] = 0
                game_board.potentialWalls = {}
                game_states['insideGame']['tryingToCapture'] = False
                mainPlayer.render(screen, game_states['insideGame']['tryingToCapture'])
            if playerRect.colliderect(enemyOneRect) and naruto == True:
            #if foundQIX(floor(mainPlayer.player_coords['x']/50), floor(mainPlayer.player_coords['y']/50), floor(game_board.enemyInfo['x']/50), floor(game_board.enemyInfo['y']/50)):
                game_states['insideGame']['lives'] = game_states['insideGame']['lives'] - 1
                mainPlayer.player_coords['x'] = 0
                mainPlayer.player_coords['y'] = 0
                if abs(enemyOne.x - mainPlayer.player_coords['x']) <= 45 and abs(enemyOne.y - mainPlayer.player_coords['x']) <= 45:
                    mainPlayer.player_coords['x'] = 950
                    mainPlayer.player_coords['y'] = 450
                game_board.potentialWalls = {}
                game_states['insideGame']['tryingToCapture'] = False
                mainPlayer.render(screen, game_states['insideGame']['tryingToCapture'])
            elif naruto == False:
                game_states['insideGame']['lives'] = game_states['insideGame']['lives'] - 1
                mainPlayer.player_coords['x'] = 0
                mainPlayer.player_coords['y'] = 0
                game_board.potentialWalls = {}
                game_states['insideGame']['tryingToCapture'] = False
                mainPlayer.render(screen, game_states['insideGame']['tryingToCapture'])
            ### Render status bar
            if game_states['insideGame']['tryingToCapture']: GAME_FONT.render_to(screen, (0, game_board_height), "Trying to Capture!", (255, 0, 0))
            if not game_states['insideGame']['tryingToCapture']: GAME_FONT.render_to(screen, (0, game_board_height), "Not trying to Capture!", (0, 255, 40))

            # areaCapturedPercentage = "{:.2f}".format(game_states['insideGame']['area'])
            GAME_FONT.render_to(screen, (0, game_board_height + 75), "captured {:.2f} percent of area".format(game_states['insideGame']['area']), (0, 0, 0))
            for x in range(game_states['insideGame']['lives']):
                screen.blit(heart, (floor(game_board_width/2) + x*75, game_board_height + 10 ))
        
        elif game_states['insideGame']['lives'] <= 0: # lose
            mainPlayer = Player()
            qixEnemy = QixEnemy(enemy_x, enemy_y, enemy_speed, enemy_speed, 25, (139, 0, 139))
            game_board = GameBoard({
                'screen_width': game_board_width,
                'screen_height': game_board_height,
                'wall_size': block_size,
                'enemy': qixEnemy
            })
            game_states = {
                'running': True,
                'outsideGame': False,
                'insideGame': { # in menu or in game
                    'tryingToCapture': False,
                    'lives': 3,
                    'area': 0
                },
                'wonRound': False,
                'startedOnce': True
            }
            ###spark
            enemyOne.x, enemyOne.y = 450, 0
            ###sparkTwo
            enemyTwo.x, enemyTwo.y = 450, 0
        else: # win 
            mainPlayer = Player()
            qixEnemy = QixEnemy(enemy_x, enemy_y, enemy_speed, enemy_speed, 25, (139, 0, 139))
            game_board = GameBoard({
                'screen_width': game_board_width,
                'screen_height': game_board_height,
                'wall_size': block_size,
                'enemy': qixEnemy
            })
            game_states = {
                'running': True,
                'outsideGame': False,
                'insideGame': { # in menu or in game
                    'tryingToCapture': False,
                    'lives': 3,
                    'area': 0
                },
                'wonRound': True,
                'startedOnce': True
            }
            ###spark
            enemyOne.x, enemyOne.y = 450, 0
            ###sparkTwo
            enemyTwo.x, enemyTwo.y = 450, 0
    else:
        ### Show Menu
        for event in pygame.event.get():
            if event.type == QUIT:
                game_states['running'] = False
            # handle keyboard input
            pressed_keys = pygame.key.get_pressed()        
            
            if pressed_keys[K_RETURN]:
                game_states['outsideGame'] = True
                game_states['wonRound'] = False
        
        screen.fill((0, 0, 0))
        
        if game_states['startedOnce']:
            if game_states['wonRound']: GAME_FONT.render_to(screen, (0, game_board_height), "You Won Try Again", (106,90,205))
            else: GAME_FONT.render_to(screen, (0, game_board_height), "You Lost Try Again", (178,132,190))

        game_menu.render(screen, GAME_FONT)


    # limit to 24fps
    # dt = clock.tick(24)
    pygame.display.update()

def resetGameB(bool):
    mainPlayer = Player()
    
    qixEnemy = QixEnemy(enemy_x, enemy_y, enemy_speed, enemy_speed, 25, (139, 0, 139))
    game_board = GameBoard({
        'screen_width': game_board_width,
        'screen_height': game_board_height,
        'wall_size': block_size,
        'enemyConfig': {
            'size': enemy_size,
            'x': 300,
            'y': 300,
        },
        'enemy': qixEnemy
    })
    game_states = {
        'running': True,
        'outsideGame': False,
        'insideGame': { # in menu or in game
            'tryingToCapture': False,
            'lives': 3,
            'area': 0
        },
        'wonRound': bool,
        'startedOnce': True
    }
    ###spark
    enemyOne.x, enemyOne.y = 450, 0
    ###sparkTwo
    enemyTwo.x, enemyTwo.y = 450, 0
