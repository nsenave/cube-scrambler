import enum
import random
from collections import deque

import argparse

class MoveName(enum.Enum):
    FRONT = 'F'
    BACK = 'B'
    RIGHT = 'R'
    LEFT = 'L'
    UP = 'U'
    DOWN = 'D'

INVERSION = "'"

class MoveSequence:

    MOVE_NAMES = [move.value for move in MoveName]
    MOVE_NAMES_COUNT = len(MOVE_NAMES)

    def pick_a_move_name():
        return MoveSequence.MOVE_NAMES[random.randrange(0, MoveSequence.MOVE_NAMES_COUNT)]

    def invert_or_not():
        return '' if random.randint(0,1) == 0 else INVERSION

    def generate_move():
        return MoveSequence.pick_a_move_name() + MoveSequence.invert_or_not()

    def are_opposite(move1, move2):
        return (move1[0] == move2[0]) and (len(move1) != len(move2))

    def is_three_quarter_turn(move1, move2, move3):
        return move1 == move2 and move2 == move3

    def is_full_turn(move1, move2, move3, move4):
        return move1 == move2 and move2 == move3 and move3 == move4

    def should_reroll(move: str, previous_moves: deque, no_half_turns=False) -> bool:
        previous_length = len(previous_moves)
        # No previous moves
        if previous_length < 1:
            return False
        # Is last move the same? (if no half move option is activated)
        previous = previous_moves[-1]
        if no_half_turns and (move == previous):
            return True
        # Is last move the opposite?
        if MoveSequence.are_opposite(move, previous):
            return True
        # If there are two previous moves: are these all the same? (to prevent three quarter turns)
        if previous_length < 2:
            return False
        previous2 = previous_moves[-2]
        if MoveSequence.is_three_quarter_turn(move, previous, previous2):
            return True
        # If there are three previous moves: are these all the same? (to prevent full turns)
        if previous_length < 3:
            return False
        previous3 = previous_moves[-3]
        return MoveSequence.is_full_turn(move, previous, previous2, previous3)

    def generate_next_move(previous_moves: deque, no_half_turns=False):
        move = MoveSequence.pick_a_move_name() + MoveSequence.invert_or_not()
        if MoveSequence.should_reroll(move, previous_moves, no_half_turns):
            return MoveSequence.generate_next_move(previous_moves, no_half_turns)
        return move

    def generate_sequence(length: int, no_half_turns=False) -> list:
        if length <= 0:
            return []
        move = MoveSequence.generate_move()
        sequence = [move]
        previous_moves = deque([move], maxlen=3)
        for _ in range(length - 1):
            move = MoveSequence.generate_next_move(previous_moves, no_half_turns)
            sequence.append(move)
            previous_moves.append(move)
        return sequence

    def __init__(self, length: int, no_half_turns=False):
        self.sequence = MoveSequence.generate_sequence(length, no_half_turns)

    def __str__(self):
        return ', '.join(self.sequence)

if __name__ == "__main__":
    # https://arxiv.org/html/2410.20630v1
    # https://math.stackexchange.com/questions/816055/minimum-number-of-random-moves-needed-to-uniformly-scramble-a-rubiks-cube
    DEFAULT_LENGTH = 25

    parser = argparse.ArgumentParser(
        description="Generates a random sequence of moves to scramble a Rubik's cube.")
    parser.add_argument(
        '-l', '--length', 
        type=int, default=DEFAULT_LENGTH, 
        help="Sequence length. If not given, the script has a default value.")
    parser.add_argument(
        '--no-half-turns', 
        action="store_true", 
        help="Prevents half turns in the sequence.")
    args = parser.parse_args()

    print(MoveSequence(length=args.length, no_half_turns=args.no_half_turns))

# https://shuffle.akselipalen.com/

# ---
# Further ideas
# Backend program that simulates Rubik's cube state. Move => updates state.
# Frontend program to vizualize it.

"""
Use cases:
- Text input => generated sequence in format like "F, U, R, U', R', F'"
- Button "Apply" => applies the moves on screen
- Sliders to vary move speed, time between moves

Smart use case:
- What should be my next move? / Hint, based on the official Rubik's solving guide.

Note:
- 20 = "God's number". Any state can be reached from any state in 20 quarter moves.

> The term "devil's algorithm" describes a move sequence which, during execution, 
> will go through all possible 43,252,003,274,489,856,000 states of the 3x3x3 Rubik's 
> cube without visiting any state more than once. 
> That is, every possible state will be equally likely when executing the sequence.

Questions:
Are there resources that gives a fast-solving sequence from any cube state?
"""
