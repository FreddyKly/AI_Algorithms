import random
import time

class Board():

    def __init__(self) -> None:
        
        self.num_white_pieces = 9 # pieces that have not been played 
        self.num_black_pieces = 9

        self.possible_positions = [
            11, 12, 13, 14, 15, 16, 17, 18,
            21, 22, 23, 24, 25, 26, 27, 28,
            31, 32, 33, 34, 35, 36, 37, 38
            ]

        self.mill_positions = [
            (11, 12, 13), (13, 14, 15), (15, 16, 17), (17, 18, 11),
            (21, 22, 23), (23, 24, 25), (25, 26, 27), (27, 28, 21),
            (31, 32, 33), (33, 34, 35), (35, 36, 37), (37, 38, 31),
            (12, 22, 32), (14, 24, 34), (16, 26, 36), (18, 28, 38)
            ]

        self.white_positions = []

        self.black_positions = []

def AI_turn(borad):
    ai_turn_pos = MCTS() 
    random.randint(0, len(possible_positions))
    possible_positions.pop(ai_turn_pos)

def Human_turn(board):
    user_turn_pos = int(input("Enter Position where you want to place a piece on: "))
    if user_turn_pos in board.possible_positions:
        num_white_pieces = num_white_pieces - 1
        board.possible_positions.pop(user_turn_pos)
        board.white_positions.append(user_turn_pos)
        if is_mill(board.white_positions):
            remove_piece_pos = int(input("You Have a Mill! Enter the position of the piece you want to be removed: "))

            while remove_piece_pos not in board.black_positions: 
                print("The position you selected is not one with a black piece on it. Try again.") 
                print("Black pieces on the Board: ", board.black_positions)
                remove_piece_pos = int(input("Enter the position of the piece you want to be removed: "))

            board.black_positions.remove(remove_piece_pos)
    else:
        print("The position you selected was not available. Try again: ")
        Human_turn()
        return

def is_mill(positions):
    return any(set(tuple).issubset(positions) for tuple in board.mill_positions)
    

class MCTS():

    def __init__(self, board) -> None:
        self.board = board

    def play_round(self):
        root = Node(None, self.board.possible_positions)
        while time.time() + 5 > time.time():
            leaf = self.selectNode(root)
            child = self.expand(leaf)
            result = self.simulate(child)

    def simulate(self, node):
        while True:
            if node.is_terminal():
                reward = node.get_score()
                return reward
            node = node.find_random_child()



class Node():
    def __init__(self, parent, children) -> None:
        self.parent = parent
        self.children = children

    def is_terminal():
        pass

    def get_score():
        pass

    def find_random_child():
        pass

if __name__ == "__main__":
    board = Board()
    print("You will be playing Nine Men's Morris as White against a AI powered by MCTS!")
    while True:
        print("Available positions: ", board.possible_positions)
        if board.num_white_pieces + board.num_black_pieces == 0:
            print("White has " + len(board.white_positions) + " pieces on the board.")
            print("Black has " + len(board.black_positions) + " pieces on the board.")
            if len(board.white_positions) > len(board.black_positions):
                print("You won!")
            elif len(board.black_positions) > len(board.white_positions):
                print("Snap! You lost :(")
            else:
                print("That's a draw.")
            break
        Human_turn(board)
        AI_turn(board)
    