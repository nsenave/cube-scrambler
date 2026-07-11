import enum
import random
from collections import deque

import argparse


# ----- Move module -----

# Notes about naming:
# "move name", "face name" or "face": the one-character name of a cube face
# "move" or "face move": a cube move like R', L2 or U

# Move are arranged so that opposites are "face to face modulo 3"
class MoveName(enum.Enum):

    FRONT = 'F'
    RIGHT = 'R'
    UP = 'U'

    BACK = 'B'
    LEFT = 'L'
    DOWN = 'D'

INVERSION = "'"

MOVE_NAMES = [move.value for move in MoveName]
MOVE_NAMES_COUNT = len(MOVE_NAMES)
MOVE_NAME_INDEX = {MOVE_NAMES[i]: i for i in range(MOVE_NAMES_COUNT)}


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

def get_direction(move):
    """
    Returns 1 for a clockwise move, -1 for a counterclockwise move.
    Note: this function implementation doesn't support with half moves.
    """
    return 1 if len(move) == 1 else -1

def are_opposite(move1, move2):
    """
    Returns true if both moves cancel each other out.
    Note: this function implementation doesn't support with half moves.
    """
    return have_same_name(move1, move2) and (get_direction(move1) != get_direction(move2))

def do_commute(move1, move2):
    name1 = get_move_name(move1)
    name2 = get_move_name(move2)
    return name1 == name2 or ((MOVE_NAME_INDEX[name1] % 3) == (MOVE_NAME_INDEX[name2] % 3))


# ----- Move sequence module -----

def count_repeat(move: str, previous_moves: deque):
    """
    Counts how many time the move is repeated in the previous moves.
    If previous moves contain a non-commutative move with the given move, 
    moves prior that are not counted.
    """
    result = 0
    for previous in reversed(previous_moves):
        if not do_commute(move, previous):
            return result
        if previous == move:
            result += 1
    return result

def contains_opposite(move: str, previous_moves: deque):
    for previous in reversed(previous_moves):
        if not do_commute(move, previous):
            return False
        if are_opposite(move, previous):
            return True
    return False

def _should_reroll(move: str, previous_moves: deque, constraints: Constraints) -> bool:
    if constraints.true_random:
        return False
    previous_length = len(previous_moves)
    if previous_length < 1:
        return False
    repeat_count = count_repeat(move, previous_moves)
    if constraints.no_half_turns and repeat_count >= 1:
        return True
    if contains_opposite(move, previous_moves):
        return True
    if previous_length < 2:
        return False
    return repeat_count >= 2

def _generate_next_move(previous_moves: deque, constraints: Constraints):
    move = pick_a_move_name() + invert_or_not()
    if _should_reroll(move, previous_moves, constraints):
        return _generate_next_move(previous_moves, constraints)
    return move

def generate_sequence(length: int, constraints: Constraints) -> list:
    if length <= 0:
        return []
    move = generate_move()
    sequence = [move]
    previous_moves = deque([move], maxlen=4)
    for _ in range(length - 1):
        move = _generate_next_move(previous_moves, constraints)
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

    STANDARD_LENGTH = 26

    def __init__(self, length: int, constraints: Constraints):
        self.sequence = generate_sequence(length, constraints)

    def __len__(self):
        return len(self.sequence)

    def __str__(self):
        return ', '.join(self.sequence)

    def print_raw(self):
        print(self.__str__())

    def print_condensed(self):
        print(', '.join(self.condensed_sequence()))

    # Inner methods serve to create the condensed sequence

    @staticmethod
    def half_turn_suffix(reduced_half_turns: int) -> str:
        match reduced_half_turns:
            case 1: return ''
            case 2: return '2'
            case 3: return INVERSION
            case _: raise ValueError(f"Unexpected reduced half turn count: {reduced_half_turns}")

    @staticmethod
    def condensed_chain(move_chain: list):
        """
        Condenses a list of moves (that are supposed to be commutative).
        """
        if len(move_chain) == 1:
            yield move_chain.pop()
        move_count = {}
        for move in move_chain:
            move_name = get_move_name(move)
            move_count[move_name] = move_count.get(move_name, 0) + get_direction(move)
        for move_name, half_turn_count in move_count.items():
            reduced_half_turns = half_turn_count % 4
            if reduced_half_turns == 0:
                continue
            yield move_name + MoveSequence.half_turn_suffix(reduced_half_turns)

    def condensed_sequence(self) -> list:
        sequence_copy = self.sequence[:]
        result = []
        while sequence_copy:
            move = sequence_copy.pop(0)
            move_chain = [move]
            while sequence_copy and do_commute(sequence_copy[0], move):
                move_chain.append(sequence_copy.pop(0))
            for condensed in MoveSequence.condensed_chain(move_chain):
                result.append(condensed)
        return result


# ----- CLI module -----

def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generates a random sequence of moves to scramble a Rubik's cube.")
    parser.add_argument(
        '-l', '--length', 
        type=int, default=MoveSequence.STANDARD_LENGTH, 
        help="Sequence length. If not given, the script has a default value.")
    parser.add_argument(
        '-c', '--condensed-notation',
        action="store_true",
        help="Shows the move sequence in condensed notation. Activated by default.")
    parser.add_argument(
        '-r', '--raw-moves',
        action="store_true",
        help="Shows raw quarter moves.")
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
    return parser.parse_args()

def should_print_raw(args):
    return args.raw_moves

def should_print_condensed(args):
    return args.condensed_notation or not args.raw_moves

if __name__ == "__main__":
    args = parse_cli_args()
    constraints = Constraints(args.no_half_turns, args.true_random)
    for _ in range(args.N):
        move_sequence = MoveSequence(args.length, constraints)
        if should_print_raw(args):
            move_sequence.print_raw()
        if should_print_condensed(args):
            move_sequence.print_condensed()
        print('')
