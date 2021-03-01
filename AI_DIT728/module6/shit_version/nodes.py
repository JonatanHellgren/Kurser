import numpy as np
import random
from states import states
"""
Here is our logical representation of the node class, it has quite a lot of
function, most of them used in the MCTS class. 
"""


class node():
    def __init__(self, state, parent=None):
        self.state = states(state)
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.ucb = np.inf

    def update_node(self, root):
        for child in self.children:
            child.ucb = child.upper_confidence_bound(root)

    def get_children(self):
        # This if-statement tells us if we need to generate circles or cross
        if np.sum(self.state.state) == 0:
            value = 1
        else:
            value = -1

        # generates the child states and saves them as children to the node
        new_states = self.state.get_legal_moves(value)
        for state in new_states:
            self.children.append(node(state, parent=self))

    def upper_confidence_bound(self, root):
        # Here we do a similar thing as in get_children(), we need to do this
        # so that the UPC will take in to account what piece is going to be laid
        if self.visits == 0:  # to avoid dividing by 0
            return np.inf
        else:
            if np.sum(self.parent.state.state) == 0:
                value = 1
            else:
                value = -1
            V = self.value / self.visits
            V *= value
            return V + 2 * np.sqrt(np.divide(np.log(root.visits), self.visits))

    def get_most_valuable_child(self):
        # This function is used when traversing the tree in the selection step
        most_valueable_child = None
        best_value = -np.inf
        if self.state.is_terminal()[0]:
            return self

        for child in self.children:
            if child.ucb == np.inf:  # if an usvisted child, return it imidetly
                return child
            # else if it is the best one so far save it
            elif best_value < child.ucb:
                best_value = child.ucb
                most_valueable_child = child

        # return the child node with highest UCB
        return most_valueable_child

    def get_most_popular_child(self):
        # get the most popular child and thus tells us wat is the next move
        highest_vistits = 0
        best_choice = None
        for child in self.children:
            if child.visits > highest_vistits:
                highest_vistits = child.visits
                best_choice = child
        return best_choice

    def increment_visits(self):
        self.visits += 1

    def is_leaf(self):
        if self.state.is_terminal()[0]:
            return True
        for child in self.children:
            if child.visits == 0:
                return True
        return False

    def ass_value(self, new_value):
        if self.visits == 0:
            self.value = new_value
        else:
            self.value += new_value
