# aßminmax
        # def aßmaxNode(alpha, beta, height, color, obsAB):
        #     bestop, bestScore = [-1,-1], alpha
        #     if height <= 0:
        #         bestScore = isWinner(obsAB)
        #         return bestop, bestScore
        #     elif not getValidMovesDict(obsAB, color):
        #         bestop, bestScore = aßminNode(alpha, beta, height-1, -color, obsAB)
        #         return  [-1,-1], bestScore
        #     m = alpha
        #     moves = getValidMovesDict(obsAB, color)
        #     for move in moves:
        #         flips = makeMove(color, move, obsAB)
        #         _, score =aßminNode(m, beta, height-1, -color, obsAB)

        #         # obsAB[move] = 0
        #         # otherTile = -color
        #         # for tile in flips:
        #         #     obsAB[tile] = otherTile

        #         if score > m:
        #             m=score
        #             bestop = move[:]
        #             bestScore = m
        #         if m >= beta:
        #             return bestop, bestScore
        #         return bestop, bestScore
        
        # def aßminNode(alpha, beta, height, color, obsAB):
        #     obsAB = obsNew.copy()
        #     bestop, bestScore = [-1,-1], beta
        #     if height <= 0:
        #         bestScore = isWinner(obsAB)
        #         return bestop, bestScore
        #     elif not getValidMovesDict(obsAB, color):
        #         bestop, bestScore = aßmaxNode(alpha, beta, height-1, -color, obsAB)
        #         return [-1,-1], bestScore
        #     m = beta
        #     moves = getValidMovesDict(obsAB, color)
        #     for move in moves:
        #         flips = makeMove(color, move, obsAB)
        #         _, score = aßmaxNode(alpha, m, height-1, -color, obsAB)

        #         # obsAB[move] = 0
        #         # otherTile = -color
        #         # for tile in flips:
        #         #     obsAB[tile] = otherTile

        #         if score < m:
        #             m=score
        #             bestop = move[:]
        #             bestScore = m
        #         if m <= alpha:
        #             return bestop, bestScore
        #     return bestop, bestScore

        # def getComputerMove(agentColor):
        #     obsAB = obsNew.copy()
        #     if agentColor == 1:
        #         move, _ = aßmaxNode(-99, 99, self.depth, agentColor, obsAB)
        #     else:
        #         move, _ = aßminNode(-99, 99, self.depth, agentColor, obsAB)
        #     return move
        
# isGoodSideMove
        # def isGoodSideMove(move, color, obsTemp) -> bool:
        #     if not isOnSide(move): return False
        #     makeMove(color, move, obsTemp)
        #     if move[1] in {0, self.rows_n-1}: func = [right, left]
        #     else: func = [up, down]
        #     move1 = move2 = move
        #     while not isOnCorner(move1) and obsTemp[func[0](move1)] == color: move1 = func[0](move1)
        #     while not isOnCorner(move2) and obsTemp[func[1](move2)] == color: move2 = func[1](move2)
        #     if isOnCorner(move1) or isOnCorner(move2): return True
        #     if obsTemp[func[0](move1)] == -color and obsTemp[func[1](move2)] == -color: return True
        #     if obsTemp[func[0](move1)] == 0 and obsTemp[func[1](move2)] == 0: 
        #         move1 = func[0](move1); move2 = func[1](move2)
        #         if isOnCorner(move1) and isOnCorner(move2): return True
        #         if isOnCorner(move1):
        #             if obsTemp[func[1](move2)] == color: return False
        #             if obsTemp[func[1](move2)] == -color: return True
        #             else: return True
        #         if isOnCorner(move2):
        #             if obsTemp[func[0](move1)] == color: return False
        #             if obsTemp[func[0](move1)] == -color: return True
        #             else: return True
        #         if obsTemp[func[0](move1)] == color or obsTemp[func[1](move2)] == color: return False
        #         if obsTemp[func[0](move1)] == -color or obsTemp[func[1](move2)] == -color: return True
        #         else: return True
        #     else:
        #         if obsTemp[func[0](move1)] == -color:
        #             if isGoodSideMove(func[1](move2), -color, obsTemp) or isOnCorner(func[1](move2)): return False
        #             else: return True
        #         if obsTemp[func[1](move2)] == -color:
        #             if isGoodSideMove(func[0](move1), -color, obsTemp) or isOnCorner(func[0](move1)): return False
        #             else: return True