import enum
import random

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

    def generate_next_move(previous: str):
        move = MoveSequence.pick_a_move_name() + MoveSequence.invert_or_not()
        if MoveSequence.are_opposite(previous, move):
            return MoveSequence.generate_next_move(previous)
        return move

    def generate_sequence(length: int) -> list:
        move = MoveSequence.generate_move()
        sequence = [move]
        previous = move
        for _ in range(length):
            move = MoveSequence.generate_next_move(previous)
            sequence.append(move)
            previous = move
        return sequence

    def __init__(self, length: int):
        self.sequence = MoveSequence.generate_sequence(length)

    def __str__(self):
        return ', '.join(self.sequence)

if __name__ == "__main__":
    # https://arxiv.org/html/2410.20630v1
    # https://math.stackexchange.com/questions/816055/minimum-number-of-random-moves-needed-to-uniformly-scramble-a-rubiks-cube
    print(MoveSequence(26))

# https://shuffle.akselipalen.com/

# ---
# Ideas:
# Prevent three identical quarter moves and full turns.
# Script options:
# --length, -l <number> Sequence length, if not given, the script has a default value.
# --no-half-turns Prevents half turns in the sequence.

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
