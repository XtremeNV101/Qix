from math import floor, sqrt

def printGameBoard(game_board):
    print('[')
    for row in game_board:
        print('\t[', end=' ')
        for coord in row:
            print(f"({coord['x']},{coord['y']}, w: {reduceBoolean(coord['w'])}, f: {reduceBoolean(coord['f'])})", end=" ")
        print('],')
    print(']')

def reduceBoolean(bool):
    if bool:
        return 'T'
    else:
        return 'F'

def findFloodingTarget(game_matrix):
    target = None
    for row in game_matrix:
        for tile in row:
            if tile['w'] == False and tile['f'] == False:
                target = tile
                break
        if target != None:
            break

    return target

def floodFill_breathFirstSearch(game_config, game_matrix, frontier, visited, starting_xCoord, starting_yCoord, enemyConfig):
    cf = { 'width': game_config['width'], 'height': game_config['height'], 'game_matrix': game_matrix, 'wall_size': game_config['wall_size']}
    if coordsAreValid(starting_xCoord, starting_yCoord, cf, {}):
        visited[(starting_xCoord, starting_yCoord)] = True
        frontier.append((starting_xCoord, starting_yCoord))
        while frontier:
            s = frontier.popleft()
            # if the next element is QIX, mark as found
            fq = foundQIX(s[0]*50 + 25, s[1]*50 + 25, enemyConfig['ax'], enemyConfig['ay'], enemyConfig['radius'], 15)
            if fq:
                enemyConfig['enemyFound'] = True
            
            # breath first iteration for each neigbour of the current tile
            for neighbour in [(s[0] + 1, s[1]), (s[0] - 1, s[1]), (s[0], s[1] + 1), (s[0], s[1] - 1)]:
                if neighbour not in visited and coordsAreValid(neighbour[0], neighbour[1], cf, visited):
                    visited[neighbour] = True
                    frontier.append(neighbour)

def coordsAreValid(xCoord, yCoord, config, visited):
    if (xCoord < 0 or xCoord >= floor(config['width']/config['wall_size'])):
        return False
    if (yCoord < 0 or yCoord >= floor(config['height']/config['wall_size'])):
        return False
    # go deep then wide
    if (config['game_matrix'][yCoord][xCoord]['w'] == True):
        return False
    if visited.get((xCoord, yCoord), False):
        return False

    return True

def circleIntersection(c1x, c1y, c2x, c2y, r1, r2):
    distanceBetweenC1C2 = sqrt(pow((c1x - c2x), 2) + pow((c1y - c2y), 2))
    if distanceBetweenC1C2 <= r1 + r2:
        return True
    else:
        return False

def foundQIX(xCoord, yCoord, qix_xCoord, qix_yCoord, r1, r2):
    # return xCoord == qix_xCoord and yCoord == qix_yCoord
    return circleIntersection(xCoord, yCoord, qix_xCoord, qix_yCoord, r1, r2)

# def generateGameBoard(wallMatrix):
#     matrix = []
#     for row in range(len(wallMatrix)):
#         nr = []
#         for col in range(len(wallMatrix[row])):
#             if wallMatrix[row][col] == 1:
#                 nr.append({ 'x': col, 'y': row, 'w': 'T', 'f': 'F' })
#             else:
#                 nr.append({ 'x': col, 'y': row, 'w': 'F', 'f': 'F' })
#         matrix.append(nr)
#     return matrix