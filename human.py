class Human:
    def __init__(self):
        pass

    def set_symbol(self, sym):
        self.sym = sym

    def take_action(self, env):
        while True:
            move = input(
                "enter the coordinate i,j fo your next move (i,j=0): ")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if env.is_empty(i, j):
                env.board[i, j] = self.sym
                break

    def update(self, env):
        pass

    def update_state_history(self, s):
        pass
