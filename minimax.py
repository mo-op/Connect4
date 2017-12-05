import random, copy

class Minimax(object):
    """ Minimax object that takes a current connect four board state
    """
    global RED
    global YELLOW
    global board
    global EMPTY
    global colors

    RED = 'red'
    YELLOW = 'yellow'
    board = None
    colors = [YELLOW, RED]
    EMPTY = None

    def __init__(self, state):
        # copy the board to self.board
        self.state = copy.deepcopy(state)


    def bestMove(self, depth, state, curr_player):
        """ Returns the best move (as a column number) and the associated alpha
            Calls search()
        """
        #self.board = self.copyBoard(state)
        # determine opponent's color
        if curr_player == colors[0]:
            opp_player = colors[1]
        else:
            opp_player = colors[0]

        # enumerate all legal moves
        legal_moves = {}  # will map legal move states to their alpha values
        for col in range(7):
            # if column i is a legal move...
            if self.isLegalMove(col, state):
                # make the move in column 'col' for curr_player
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.search(depth - 1, temp, opp_player)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        #print (moves)
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move
        return best_move, best_alpha

    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever
            called this search

            Returns the alpha value
        """

        # enumerate all legal moves from this state
        legal_moves = []
        for i in range(7):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # determine opponent's color
        if curr_player == colors[0]:
            opp_player = colors[1]
        else:
            opp_player = colors[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth - 1, child, opp_player))
        return alpha
################### problem
    def isLegalMove(self, column, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        #state = self.copyBoard(state)
        for i in range(6):
            if state[column][i] == ' ':
                return True
        return False

    # for x in range(7):
    #     for y in range(6):
    #         if board[x][y] == None:
    #             return False
    # return True

    def gameIsOver(self, state):
        if self.checkForStreak(state, colors[0], 4) >= 1:
            return True
        elif self.checkForStreak(state, colors[1], 4) >= 1:
            return True
        else:
            return False

    def makeMove(self, state, column, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'

            Returns a copy of new state array with the added move
        """
        temp = copy.deepcopy(state)
        for i in range(6):
            if temp[column][i] == ' ':
                temp[column][i] = color
        return temp

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 +
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == colors[0]:
            o_color = colors[1]
        else:
            o_color = colors[0]

        my_fours = self.checkForStreak(state, color, 4)
        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)
        opp_fours = self.checkForStreak(state, o_color, 4)
        # opp_threes = self.checkForStreak(state, o_color, 3)
        # opp_twos = self.checkForStreak(state, o_color, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours * 100000 + my_threes * 100 + my_twos

    def checkForStreak(self, state, color, streak):
        count = 0
        # for each piece in the board...
        for i in range(7):
            for j in range(6):
                # ...that is of the color we're looking for...
                if state[i][j].lower() == color.lower():
                    # check if a vertical streak starts at (i, j)
                    count += self.verticalStreak(i, j, state, streak)

                    # check if a horizontal four-in-a-row starts at (i, j)
                    count += self.horizontalStreak(i, j, state, streak)

                    # check if a diagonal (either way) four-in-a-row starts at (i, j)
                    count += self.diagonalCheck(i, j, state, streak)
        # return the sum of streaks of length 'streak'
        return count

    def verticalStreak(self, col, row, state, streak):
        consecutiveCount = 0
        for i in range(col, 7):
            if state[i][row].lower() == state[col][row].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalStreak(self, col, row, state, streak):
        consecutiveCount = 0
        for j in range(col, 7):
            if state[j][row].lower() == state[col][row].lower():
                consecutiveCount += 1
            else:
                break

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, col, row, state, streak):

        total = 0
        # check for diagonals with positive slope
        consecutiveCount = 0
        j = row
        for i in range(col, 7):
            if j > 5:
                break
            elif state[i][j].lower() == state[col][row].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        # check for diagonals with negative slope
        consecutiveCount = 0
        j = row
        for i in range(col, -1, -1):
            if j > 5:
                break
            elif state[i][j].lower() == state[col][row].lower():
                consecutiveCount += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutiveCount >= streak:
            total += 1

        return total
