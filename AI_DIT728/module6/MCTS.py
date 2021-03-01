import numpy as np
from nodes import node


class MCTS():
    def __init__(self, n=None):
        n = n

    def get_move(self, state):
        new_state = self.tree_search(state)
        return np.concatenate(np.where(state != new_state))

    def tree_search(self, state, iterations=10000):
        n = node(state)
        for it in range(iterations):
            n.rollout()
        print(n.children)
        for it in n.children:
            print(it.value)
            print(it.state)
        return n.get_most_valuable_child().state


def testing():
    state = np.array([[1, 0, -1], [0, 1, -1], [0, 1, 0]])
    AI = MCTS()
    print(AI.get_move(state))


testing()
