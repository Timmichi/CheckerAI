from random import randint
from BoardClasses import Board
from copy import deepcopy
from math import sqrt, log


# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
class Node():
    def __init__(self):
        self.children = {}
        self.move = None
        self.key = None
        self.board = None
        self.parent = None
        self.wins = 0
        self.passes = 0
        self.color = None

class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.startnode = Node()
        self.startnode.board = Board(col, row, p)
        self.startnode.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2
        self.maxiter = 25
        self.curriter = 0

    def get_move(self, move):
        if len(move) != 0:  # if opponent goes first, then our color stays 2 (white)
            if self.startnode.children:
                for child in self.startnode.children.values():
                    if str(child.move) == str(move):
                        self.startnode = child
                        break
            else:
                newnode = self.create_node_child(self.startnode, self.opponent[self.color], move)  # update board with opp move
                self.startnode = newnode

        else:
            self.color = 1  # if we go first, our color changes to 1 (black)'
            self.startnode.color = self.color


        color = self.color
        currnode = self.startnode
        moves = currnode.board.get_all_possible_moves(color)
        moves = self.get_possible_moves(moves)

        while self.curriter <= self.maxiter and moves != []:
            if currnode.children == {}:
                self.create_node_children(currnode, color, moves)
                self.leaf_nodes_simprop(currnode)

            # find and put the expanded node through the while loop
            currnode = self.find_expandnode(self.startnode)
            color = self.opponent[currnode.color]
            moves = currnode.board.get_all_possible_moves(color)
            moves = self.get_possible_moves(moves)
        bestnode = self.find_best_node(self.startnode)
        self.startnode = bestnode
        self.curriter = 0
        return self.startnode.move

    # ----------------------------HELPER FUNCTIONS----------------------------

    @staticmethod
    def get_possible_moves(moves):
        move_list = []
        for m_set in moves:
            for m in m_set:
                move_list.append(m)
        return move_list

    @staticmethod
    def create_node_child(node, color, move):
        newboard = deepcopy(node.board)
        newboard.make_move(move, color)
        newnode = Node()
        newnode.board = newboard
        newnode.color = color
        newnode.move = move
        return newnode
    @staticmethod
    def create_node_children(node, color, moves):
        for i, move in enumerate(moves):
            newboard = deepcopy(node.board)
            newboard.make_move(move, color)
            newnode = Node()
            newnode.board = newboard
            newnode.parent = node
            newnode.color = color
            newnode.move = move
            newnode.key = i
            node.children[newnode.key] = newnode

    @staticmethod
    def find_highest_score(node):
        maxscore = -1
        for childnode in node.children.values():
            vi = childnode.wins / childnode.passes
            z = 2 * sqrt(log(node.passes) / childnode.passes)
            score = vi + z
            if maxscore < score:
                bestnode = childnode.key
                maxscore = score
        return bestnode

    def leaf_nodes_simprop(self, node):
        for childnode in node.children.values():
            # run a simulation on a childnode
            winner = self.single_simulator(childnode)
            self.curriter += 1
            # propagate results back to actual start node and update values
            while childnode != node:
                if winner == childnode.color:
                    childnode.wins += 1
                childnode.passes += 1
                childnode = childnode.parent
            node.passes += 1

    def single_simulator(self, node):
        if node.board.is_win(node.color) == 2 or node.board.is_win(node.color) == 1:
            return node.board.is_win(node.color)
        # create a new node and make it have the opposite color of the node passed in.
        color = self.opponent[node.color]
        moves = node.board.get_all_possible_moves(color)
        index = randint(0, len(moves) - 1)
        inner_index = randint(0, len(moves[index]) - 1)
        move = moves[index][inner_index]

        newnode = Node()
        newnode.board = deepcopy(node.board)
        newnode.board.make_move(move, color)
        newnode.color = color
        return self.single_simulator(newnode)

    def find_expandnode(self, node):
        while node.children:
            key = self.find_highest_score(node)
            node = node.children[key]
        return node

    def find_best_node(self, node):
        max = -1
        bestmove = []
        for childnode in node.children.values():
            if childnode.passes > max:
                bestmove.append(childnode)
                max = childnode.passes
        return bestmove[-1]





