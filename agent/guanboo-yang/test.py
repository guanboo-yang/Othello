def isOdd(move, obs):
    def flood(move, obs):
        count = 0
        if 0 <= move[0] < 8 and 0 <= move[1] < 8:
            if obs[move] == 0:
                obs[move] = 2
                count += 1
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    count += flood((move[0] + dx, move[1] + dy), obs)
        return count
    count = flood(move, obs)
    return count % 2

def stability(obs, color):
    def countStability(move, obs, color):
        def isInBoard(move):
            if 0 <= move[0] < 8 and 0 <= move[1] < 8: return True
            else: return False
        count = 0
        if not isInBoard(move):
            return True
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if ((move[0] + dx, move[1]), obs, color) and ((move[0], move[1] + dy), obs, color):
                count += 1
                obs[move] = True
        return count
    count = sum([countStability(move, obs, color)] for move in [(0, 0), (0, 7), (7, 7), (7, 0)])
    return count

# import random
# obs = {(x, y):int(t) for x in range(8) for y in range(8) for t in [random.randint(-1, 1)]}
obs =  {(0, 0):  1, (0, 1):  1, (0, 2):  1, (0, 3):  0, (0, 4):  0, (0, 5):  1, (0, 6):  1, (0, 7):  1, 
        (1, 0):  1, (1, 1):  1, (1, 2): -1, (1, 3):  1, (1, 4):  0, (1, 5):  1, (1, 6):  1, (1, 7):  1, 
        (2, 0): -1, (2, 1): -1, (2, 2): -1, (2, 3):  1, (2, 4):  0, (2, 5):  1, (2, 6): -1, (2, 7):  1, 
        (3, 0): -1, (3, 1):  0, (3, 2): -1, (3, 3):  1, (3, 4):  0, (3, 5):  0, (3, 6):  0, (3, 7):  1, 
        (4, 0):  1, (4, 1):  0, (4, 2):  0, (4, 3): -1, (4, 4):  0, (4, 5):  1, (4, 6): -1, (4, 7):  1, 
        (5, 0):  1, (5, 1):  1, (5, 2):  0, (5, 3):  0, (5, 4):  1, (5, 5): -1, (5, 6):  0, (5, 7):  1, 
        (6, 0): -1, (6, 1):  1, (6, 2): -1, (6, 3):  0, (6, 4):  1, (6, 5): -1, (6, 6):  1, (6, 7):  1, 
        (7, 0):  1, (7, 1):  1, (7, 2):  1, (7, 3):  0, (7, 4):  1, (7, 5):  1, (7, 6):  1, (7, 7):  1}

move1 = (0, 2)
move2 = (3, 1)
move3 = (0, 4)
print(stability(move1, obs, 1))
# print(isOdd(move2, obs))
# print(isOdd(move3, obs))
# answer: 24