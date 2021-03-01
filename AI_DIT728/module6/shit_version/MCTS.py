import numpy as np
import random
from nodes import node
from states import states
"""
Here is our implementation of the MCTS algorithm, it does the things explained
in the report and pack them together with get_move() which is it's way of
comunicating with the game.
"""


class MCTS():
    def __init__(self, state):
        self.value = -1
        self.root = node(state)

    def get_move(self, state):
        self.update(state)

        for it in range(200):
            current_node = self.traverse()
            current_node.update_node(self.root)
            current_node = current_node.get_most_valuable_child()
            value = self.rollout(current_node.state)
            self.backpropagate(current_node, value)
        self.root = self.root.get_most_popular_child()

        cord = np.where(self.root.state.state != state)
        return cord

    def update(self, state):
        if self.root.children == []:
            self.root.get_children()

        for child in self.root.children:
            if (state == child.state.state).all():
                self.root = child

        if (self.root.state.state != state).any():
            print('update not working')

    def traverse(self):
        current_node = self.root

        if current_node.children == []:
            current_node.get_children()

        while not current_node.is_leaf():
            current_node.update_node(self.root)

            new_node = current_node.get_most_valuable_child()
            if new_node != None:
                current_node = new_node

            if current_node.children == []:
                current_node.get_children()

        return current_node

    def rollout(self, current_state):

        if np.sum(current_state.state == 1):
            current_value = 1
        else:
            current_value = -1

        while not current_state.is_terminal()[0]:
            current_state = states(
                random.choice(current_state.get_legal_moves(current_value)))
            current_value *= -1
        return current_state.is_terminal()[1]

    def backpropagate(self, nd, value):
        nd.ass_value(value)
        nd.increment_visits()
        while self.root != nd:
            nd.parent.ass_value(value)
            nd.parent.increment_visits()
            nd = nd.parent
