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

MOVE_NAMES = [move.value for move in MoveName]
MOVE_NAMES_COUNT = len(MOVE_NAMES)

def pick_a_move_name():
    return MOVE_NAMES[random.randrange(0, MOVE_NAMES_COUNT)]

def invert_or_not():
    return '' if random.randint(0,1) == 0 else INVERSION

def generate_move():
    return pick_a_move_name() + invert_or_not()

def get_move_name(move) -> str:
    return move[0]

def have_same_name(move1, move2):
    return get_move_name(move1) == get_move_name(move2)

def have_same_direction(move1, move2):
    """Direction means clockwise vs. counterclockwise."""
    return len(move1) == len(move2)

def should_reroll(move: str, previous_moves: deque, constraints: Constraints) -> bool:
    # If true random option, never reroll
    if constraints.true_random:
        return False
    # No previous moves
    previous_length = len(previous_moves)
    if previous_length < 1:
        return False
    # Is last move the same? (if no half move option is activated)
    previous = previous_moves[-1]
    have_same_name_as_previous = have_same_name(move, previous)
    have_same_direction_as_previous = have_same_direction(move, previous)
    is_same_as_previous = have_same_name_as_previous and have_same_direction_as_previous
    if constraints.no_half_turns and is_same_as_previous:
        return True
    # Is last move the opposite?
    if have_same_name_as_previous and not have_same_direction_as_previous:
        return True
    # If there are two previous moves: are these all the same? (to prevent three quarter turns or more)
    if previous_length < 2:
        return False
    previous2 = previous_moves[-2]
    return is_same_as_previous and (previous == previous2)

def generate_next_move(previous_moves: deque, constraints: Constraints):
    move = pick_a_move_name() + invert_or_not()
    if should_reroll(move, previous_moves, constraints):
        return generate_next_move(previous_moves, constraints)
    return move

def generate_sequence(length: int, constraints: Constraints) -> list:
    if length <= 0:
        return []
    move = generate_move()
    sequence = [move]
    previous_moves = deque([move], maxlen=3)
    for _ in range(length - 1):
        move = generate_next_move(previous_moves, constraints)
        sequence.append(move)
        previous_moves.append(move)
    return sequence


class Constraints:

    def __init__(self, no_half_turns=False, true_random=False):
        self.no_half_turns = no_half_turns
        self.true_random = true_random
        self.coherence_check()

    def coherence_check(self):
        if self.true_random and self.no_half_turns:
            raise ValueError("'True random' implies that half turn are allowed.")


class MoveSequence:

    def __init__(self, length: int, constraints: Constraints, condensed_notation: bool):
        self.sequence = generate_sequence(length, constraints)
        self.condensed_notation = condensed_notation

    def __str__(self):
        return ', '.join(self.condensed_sequence() if self.condensed_notation else self.sequence)

    def condensed_sequence(self) -> list:
        sequence_copy = self.sequence[:]
        result = []
        while sequence_copy:
            move = sequence_copy.pop(0)
            move_chain = [move]
            while sequence_copy and sequence_copy[0] == move:
                move_chain.append(sequence_copy.pop(0))
            chain_length = len(move_chain)
            if chain_length == 1:
                result.append(move)
            else:
                if chain_length % 2 == 0:
                    result.append(get_move_name(move) + str(chain_length))
                else:
                    result.append(move + str(chain_length))
        return result


if __name__ == "__main__":
    # https://arxiv.org/html/2410.20630v1
    # https://math.stackexchange.com/questions/816055/minimum-number-of-random-moves-needed-to-uniformly-scramble-a-rubiks-cube
    DEFAULT_LENGTH = 26

    parser = argparse.ArgumentParser(
        description="Generates a random sequence of moves to scramble a Rubik's cube.")
    parser.add_argument(
        '-l', '--length', 
        type=int, default=DEFAULT_LENGTH, 
        help="Sequence length. If not given, the script has a default value.")
    parser.add_argument(
        '-c', '--condensed-notation',
        action="store_true",
        help="Prints U2 instead of U, U for instance.")
    parser.add_argument(
        '--no-half-turns', 
        action="store_true", 
        help="Prevents half turns in the sequence.")
    parser.add_argument(
        '--true-random', 
        action="store_true",
        help="No constraint on move generation (allows moves that directly cancel each other out).")
    parser.add_argument(
        '-N',
        type=int, default=1, 
        help="Number of sequences to print (defaults to 1).")
    args = parser.parse_args()

    constraints = Constraints(args.no_half_turns, args.true_random)
    for _ in range(args.N):
        print(MoveSequence(args.length, constraints, args.condensed_notation))

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
- 20 = "God's number". Any state can be reached from any state in 20 quarter or half moves.
- It's 26 if half moves are counted as two quarter moves.

> The term "devil's algorithm" describes a move sequence which, during execution, 
> will go through all possible 43,252,003,274,489,856,000 states of the 3x3x3 Rubik's 
> cube without visiting any state more than once. 
> That is, every possible state will be equally likely when executing the sequence.

Questions:
Are there resources that gives a fast-solving sequence from any cube state?
"""
