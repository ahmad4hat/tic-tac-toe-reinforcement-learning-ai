import numpy


class Environment:
    def __init__(self, length=3):
        self.length = length
        self.board = numpy.zeros((length, length))
        # 1 and -1 is choose for easier calculation of winning the game
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.number_of_state = 3**(self.length*self.length)

    def is_empty(self, i, j):  # i ,j is the position of tic- tac toe boards
        return self.board[i, j] == 0

    def reward(self, sym):
        print(sym)
        if not self.game_over():
            return 0
        # if(sym == self.winner):
        #     print(f"winner is {self.winner}")
        return 1 if self.winner == sym else 0

    def get_state(self):
        state_integer_representation = 0
        position_integer_representation = 0
        for i in range(self.length):
            for j in range(self.length):
                if self.board[i, j] == 0:
                    box_stuff = 0
                elif self.board[i, j] == self.x:
                    box_stuff = 1
                elif self.board[i, j] == self.o:
                    box_stuff = 2
                state_integer_representation += (
                    3**position_integer_representation)*box_stuff
                position_integer_representation += 1
        return state_integer_representation

    def game_over(self, force_recalculate=False):
        if not force_recalculate and self.ended:
            return self.ended
        # check rows
        for i in range(self.length):
            for player in (self.x, self.o):  # (self.x,self.o) is a tuple
                if self.board[i].sum() == player * self.length:
                    self.winner = player
                    self.ended = True
                    return True
        # check colum
        for j in range(self.length):
            for player in (self.x, self.o):  # (self.x,self.o) is a tuple
                if self.board[:, j].sum() == player * self.length:
                    self.winner = player
                    self.ended = True
                    return True
        # check diagonals
        for player in (self.x, self.o):
            if self.board.trace() == player*self.length:  # trace add diagonals in array
                self.winner = player
                self.ended = True
                return True
            # trace add diagonals in array
            if numpy.fliplr(self.board).trace() == player*self.length:  # flipr flips the board
                self.winner = player
                self.ended = True
                return True

            if numpy.all((self.board == 0) == False):
                self.winner = None
                self.ended = True
                return True
        self.winner = None
        return False

    def is_draw(self):
        return self.ended and self.winner is None

    def reward(self, player):
        if not self.game_over():
            return 0
        # if self.winner == player:
        #     print("winner is")
        #     print(player)
        return 1 if self.winner == player else 0

    def draw_board(self):
        for i in range(self.length):
            print("----------")
            for j in range(self.length):
                print("| ", end="")  # end = " " for not creating a new line
                if self.board[i, j] == self.x:
                    print("x", end="")
                elif self.board[i, j] == self.o:
                    print("o", end="")
                else:
                    print(" ", end="")
            print("|")
        print("----------")
