import numpy as np
import random


class node():
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.unvisited_children = []

    def rollout(self):
        is_terminal, value = self.check_terminal()
        n = self
        while not is_terminal:
            n = n.explore()
            is_terminal, value = n.check_terminal()
        n.backpropagate(value)

    def explore(self):
        if self.children == []:
            self.get_children()
        #self.update_node()
        return random.choice(self.children)

    def check_terminal(self):
        row_sums = np.sum(self.state, axis=0)
        col_sums = np.sum(self.state, axis=1)
        dig_sum1 = self.state[0, 0] + self.state[1, 1] + self.state[2, 2]
        dig_sum2 = self.state[0, 2] + self.state[1, 1] + self.state[2, 0]
        if 3 in row_sums or 3 in col_sums or 3 == dig_sum1 or 3 == dig_sum2:
            return [True, -20]
        elif -3 in row_sums or -3 in col_sums or -3 == dig_sum1 or -3 == dig_sum2:
            return [True, 10]
        else:
            if 0 not in self.state:
                return [True, 0]
            else:
                return [False, 0]

    def backpropagate(self, value):
        node = self
        node.ass_value(value)
        node.increment_visits()
        while (node.parent != None):
            node.parent.ass_value(value)
            node.parent.increment_visits()
            node = node.parent

    def get_children(self):
        new_states = legal_moves(self.state)
        for state in new_states:
            self.children.append(node(state, parent=self))

    def upper_confidence_bound(self):
        if self.visits == 0:  # to avoid dividing by 0
            return -np.inf
        else:
            V = self.value / self.visits
            return V + 2 * np.sqrt(
                np.divide(np.log(self.parent.visits), self.visits))

    def update_node(self):
        for child in self.children:
            child.ass_value(child.upper_confidence_bound())
            if child.value == -np.inf:
                self.unvisited_children.append(child)

    def get_most_valuable_child(self):
        most_valueable_child = None
        best_value = -np.inf
        for child in self.children:
            if best_value < child.value:
                best_value = child.value
                most_valueable_child = child
        return most_valueable_child

    def increment_visits(self):
        self.visits += 1

    def ass_value(self, new_value):
        if self.value == -np.inf:
            self.value = new_value
        else:
            self.value += new_value


"""
def main():
    state = np.array([[-1, 1, -1], [0, -1, 1], [1, -1, 1]])
    state = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    n = node(state)

    n.monte_carlo_search()
    ne = n.get_most_valuable_child()
    print(ne.state)
"""


def legal_moves(state):
    symbol = get_symbol(state)
    legal = []
    for ix, row in enumerate(state):
        for jx, cell in enumerate(row):
            if cell == 0:
                tmp_state = np.copy(state)
                tmp_state[ix, jx] = symbol
                legal.append(tmp_state)
    return legal


def get_symbol(state):
    if np.sum(state) == 1:  # if one more circle (assuming circle starts)
        return -1  # cross
    else:  # if equal amounts of circle and crosses
        return 1  # circle
