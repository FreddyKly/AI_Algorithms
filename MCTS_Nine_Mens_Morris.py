import random
import time

num_white_pieces = 9 # pieces that have not been played 
num_black_pieces = 9

possible_positions = [
    11, 12, 13, 14, 15, 16, 17, 18,
    21, 22, 23, 24, 25, 26, 27, 28,
    31, 32, 33, 34, 35, 36, 37, 38
    ]

mill_positions = [
    (11, 12, 13), (13, 14, 15), (15, 16, 17), (17, 18, 11),
    (21, 22, 23), (23, 24, 25), (25, 26, 27), (27, 28, 21),
    (31, 32, 33), (33, 34, 35), (35, 36, 37), (37, 38, 31),
    (12, 22, 32), (14, 24, 34), (16, 26, 36), (18, 28, 38)
    ]

white_positions = []

black_positions = []

def AI_turn():
    ai_turn_pos = MCTS() 
    random.randint(0, len(possible_positions))
    possible_positions.pop(ai_turn_pos)

def Human_turn():
    user_turn_pos = int(input("Enter Position where you want to place a piece on: "))
    if user_turn_pos in possible_positions:
        num_white_pieces = num_white_pieces - 1
        possible_positions.pop(user_turn_pos)
        white_positions.append(user_turn_pos)
        if is_mill(white_positions):
            remove_piece_pos = int(input("You Have a Mill! Enter the position of the piece you want to be removed: "))

            while remove_piece_pos not in black_positions: 
                print("The position you selected is not one with a black piece on it. Try again.") 
                print("Black pieces on the Board: ", black_positions)
                remove_piece_pos = int(input("Enter the position of the piece you want to be removed: "))

            black_positions.remove(remove_piece_pos)
    else:
        print("The position you selected was not available. Try again: ")
        Human_turn()
        return

def is_mill(positions):
    return any(set(tuple).issubset(positions) for tuple in mill_positions)
    

class MCTS():
    def play_round():
        root = Node(None, possible_positions)
        while time.time() + 5 > time.time():
            leaf = root.selectNode()
            child = leaf.expand()
            result = child.simulate()



class Node():
    def __init__(self, parent, children) -> None:
        self.parent = parent
        self.children = children

if __name__ == "__main__":
    print("You will be playing Nine Men's Morris as White against a AI powered by MCTS!")
    while True:
        print("Available positions: ", possible_positions)
        if num_white_pieces + num_black_pieces == 0:
            print("White has " + len(white_positions) + " pieces on the board.")
            print("Black has " + len(black_positions) + " pieces on the board.")
            if len(white_positions) > len(black_positions):
                print("You won!")
            elif len(black_positions) > len(white_positions):
                print("Snap! You lost :(")
            else:
                print("That's a draw.")
            break
        Human_turn()
        AI_turn()
    