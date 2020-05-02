
import numpy


class Agent:
    # eps(exploration/ expoitation) is the epilon greedy value, aplpha is the learning rate
    def __init__(self, eps=0.01, alpha=0.5, length=3):
        self.eps = eps
        self.length = length
        self.alpha = alpha
        self.state_history = []
        self.verbose = False

    def setV(self, V):
        self.V = V

    def set_symbol(self, sym):
        self.sym = sym

    def set_verbose(self, verbose):
        self.verbose = verbose

    def reset_story(self):
        self.state_history = []

    def take_action(self, env):
        r = numpy.random.rand()
        best_state = None
        if r < self.eps:
            if self.verbose:
                print("taking random action")

            possible_moves = []
            for i in range(self.length):
                for j in range(self.length):
                    if env.is_empty(i, j):
                        possible_moves.append((i, j))

            idx = numpy.random.choice(len(possible_moves))

            next_move = possible_moves[idx]
        else:
            pos2value = {}
            next_move = None
            best_value = -1
            for i in range(self.length):
                for j in range(self.length):
                    if env.is_empty(i, j):
                        env.board[i, j] = self.sym
                        state = env.get_state()
                        env.board[i, j] = 0
                        pos2value[(i, j)] = self.V[state]
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i, j)
            # print(self.V)

            # if self.verbose:
            #     print("taking greedy action")
            #     for i in range(self.length):
            #         print("----------")
            #         for j in range(self.length):
            #             if env.is_empty(i, j):
            #                 print(f"{pos2value[(i,j)]}", end="")
            #             # end = " " for not creating a new line
            #             else:
            #                 print("| ", end="")
            #                 if env.board[i, j] == env.x:
            #                     print("x", end="")
            #                 elif env.board[i, j] == env.o:
            #                     print("o", end="")
            #                 else:
            #                     print(" ", end="")
            #         print("|")
            #     print("----------")
            if self.verbose:
                print("Taking a greedy action")
                for i in range(self.length):
                    print("------------------")
                    for j in range(self.length):
                        if env.is_empty(i, j):
                            # print the value

                            print(f"| {pos2value[(i,j)]:.2f}", end="")
                        else:
                            print("  ", end="")
                            if env.board[i, j] == env.x:
                                print("x  |", end="")
                            elif env.board[i, j] == env.o:
                                print("o  |", end="")
                            else:
                                print("   |", end="")
                    print("")
        env.board[next_move[0], next_move[1]] = self.sym

    def update_state_history(self, new_state):
        self.state_history.append(new_state)

    def update(self, env):
        # print("update")
        reward = env.reward(self.sym)
        # print(f"reward {reward}")
        # print(self.state_history)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha*(target-self.V[prev])
            self.V[prev] = value
            target = value
        # print(self.V)
        self.reset_story()
