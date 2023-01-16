import random

num_white_pieces = 9
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
    ai_turn_pos = random.randint(0, len(possible_positions))
    possible_positions.pop(ai_turn_pos)

def Human_turn():
    user_turn_pos = int(input("Enter Position where you want to place a piece on: "))
    if user_turn_pos in possible_positions:
        num_white_pieces = num_white_pieces - 1
        possible_positions.pop(user_turn_pos)
        white_positions.append(user_turn_pos)
        if is_mill(white_positions):
            print("Black pieces on the Board: ", black_positions)
            removed_piece = int(input("Enter the position of the piece you  want to tbe removed: "))
    else:
        print("The position you selected was not available. Try again: ")
        Human_turn()
        return

def is_mill(positions):
    pass

def remove_piece():
    pass

def MCTS():
    pass 

if __name__ == "__main__":
    print("You will be playing Nine Men's Morris as White against a AI powered by MCTS!")
    while True:
        print("Available positions: ", possible_positions)
        Human_turn()
        AI_turn()
        MCTS()
    