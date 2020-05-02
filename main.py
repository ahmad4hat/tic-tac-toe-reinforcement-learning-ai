import numpy
from enviroment import Environment
from agent import Agent
from human import Human


# def get_state_hash_and_winner(env, i=0, j=0):
#     results = []

#     for v in (0, env.x, env.o):
#         env.board[i, j] = v
#         if j == 2:
#             if i == 2:
#                 state = env.get_state()
#                 ended = env.game_over(force_recalcute=False)
#                 winner = env.winner
#             else:
#                 results += get_state_hash_and_winner(env, i+1, 0)
#         else:
#             results += get_state_hash_and_winner(env, i, j+1)
#     return results
def get_state_hash_and_winner(env, i=0, j=0):
    results = []

    for v in (0, env.x, env.o):
        env.board[i, j] = v  # if empty board it should already be 0
        if j == 2:
            # j goes back to 0, increase i, unless i = 2, then we are done
            if i == 2:
                # the board is full, collect results and return
                state = env.get_state()
                ended = env.game_over(force_recalculate=True)
                winner = env.winner
                results.append((state, winner, ended))
            else:
                results += get_state_hash_and_winner(env, i + 1, 0)
        else:
            # increment j, i stays the same
            results += get_state_hash_and_winner(env, i, j + 1)

    return results


def initalV_x(env, state_winnder_triples):
    V = numpy.zeros(env.number_of_state)
    for state, winner, ended in state_winnder_triples:
        if ended:
            if winner == env.x:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V


def initalV_o(env, state_winnder_triples):
    V = numpy.zeros(env.number_of_state)
    for state, winner, ended in state_winnder_triples:
        if ended:
            if winner == env.o:
                v = 1
            else:
                v = 0
        else:
            v = 0.5
        V[state] = v
    return V


def play_game(p1, p2, env, draw=False):
    current_player = None
    while not env.game_over():
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1

        if draw:
            if draw == 1 and current_player == p1:
                env.draw_board()
            if draw == 2 and current_player == p2:
                env.draw_board()
        current_player.take_action(env)
        state = env.get_state()
        p1.update_state_history(state)
        p2.update_state_history(state)

    if draw:
        env.draw_board()

    p1.update(env)
    p2.update(env)


p1 = Agent()
p2 = Agent()

env = Environment()
state_winnder_triple = get_state_hash_and_winner(env)

Vx = initalV_x(env, state_winnder_triple)
# print(Vx)
p1.setV(Vx)
Vo = initalV_o(env, state_winnder_triple)
p2.setV(Vo)

print(Vx)
print(Vo)
print(len(Vx))
print(len(Vo))

p1.set_symbol(env.x)
p2.set_symbol(env.o)

T = 100000
for t in range(T):
    if t % 200 == 0:
        print(t)
    play_game(p1, p2, Environment())

human = Human()
human.set_symbol(env.o)
while True:
    p1.set_verbose(True)
    play_game(p1, human, Environment(), draw=2)
    answer = input("play again > [Y/n]")
    if answer and answer.lower()[0] == 'n':
        break
