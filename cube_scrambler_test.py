import cube_scrambler
from collections import deque
import unittest


class TestUtils:

    def yield_inversions(move_name1, move_name2):
        yield (move_name1, move_name2)
        yield (move_name1, move_name2 + "'")
        yield (move_name1 + "'", move_name2)
        yield (move_name1 + "'", move_name2 + "'")


class CubeScramblerTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_pick_a_move_name(self):
        expected = ('U', 'D', 'F', 'B', 'R', 'L')
        for _ in range(20):
            self.assertTrue(cube_scrambler.pick_a_move_name() in expected)

    def test_invert_or_not(self):
        expected = ('', "'")
        for _ in range(20):
            self.assertTrue(cube_scrambler.invert_or_not() in expected)

    def test_generate_move(self):
        for _ in range(20):
            move = cube_scrambler.generate_move()
            self.assertIsInstance(move, str)
            length = len(move)
            self.assertTrue(length == 1 or length == 2)
            # the function is designed to generate quarter moves only
            if length == 2:
                self.assertEndsWith(move, "'")
            self.assertFalse('2' in move)

    def test_get_move_name(self):
        self.assertEqual('U', cube_scrambler.get_move_name('U'))
        self.assertEqual('L', cube_scrambler.get_move_name("L'"))

    def test_have_same_name(self):
        self.assertTrue(cube_scrambler.have_same_name('R', 'R'))
        self.assertTrue(cube_scrambler.have_same_name('D', "D'"))
        self.assertTrue(cube_scrambler.have_same_name("D'", "D'"))
        self.assertFalse(cube_scrambler.have_same_name('R', 'U'))
        self.assertFalse(cube_scrambler.have_same_name('R', "U'"))
        self.assertFalse(cube_scrambler.have_same_name("D'", "U'"))

    def test_get_direction(self):
        self.assertEqual(1, cube_scrambler.get_direction('U'))
        self.assertEqual(1, cube_scrambler.get_direction('D'))
        self.assertEqual(-1, cube_scrambler.get_direction("U'"))
        self.assertEqual(-1, cube_scrambler.get_direction("D'"))

    def test_are_opposite(self):
        self.assertTrue(cube_scrambler.are_opposite('U', "U'"))
        self.assertFalse(cube_scrambler.are_opposite('U', 'U'))
        self.assertFalse(cube_scrambler.are_opposite('U', 'D'))
        self.assertFalse(cube_scrambler.are_opposite('U', "D'"))
        self.assertFalse(cube_scrambler.are_opposite('U', 'F'))
        self.assertFalse(cube_scrambler.are_opposite('U', "F'"))

    def assertCommuteWithInversions(self, move_name1, move_name2):
        for move1, move2 in TestUtils.yield_inversions(move_name1, move_name2):
            self.assertTrue(cube_scrambler.do_commute(move1, move2))

    def assertCommuteWithPermutation(self, move_name1, move_name2):
        self.assertCommuteWithInversions(move_name1, move_name2)
        self.assertCommuteWithInversions(move_name2, move_name1)

    def assertDontCommuteWithInversions(self, move_name1, move_name2):
        for move1, move2 in TestUtils.yield_inversions(move_name1, move_name2):
            self.assertFalse(cube_scrambler.do_commute(move1, move2))

    def assertDontCommuteWithPermutation(self, move_name1, move_name2):
        self.assertDontCommuteWithInversions(move_name1, move_name2)
        self.assertDontCommuteWithInversions(move_name2, move_name1)

    def test_do_commute(self):
        for move_name in ('U', 'D', 'F', 'B', 'R', 'L'):
            self.assertCommuteWithInversions(move_name, move_name)
        self.assertCommuteWithPermutation('U', 'D')
        self.assertCommuteWithPermutation('F', 'B')
        self.assertCommuteWithPermutation('R', 'L')
        for move_name in ('F', 'B', 'R', 'L'):
            self.assertDontCommuteWithPermutation('U', move_name)

    def test_count_repeat(self):
        self.assertEqual(0, cube_scrambler.count_repeat('U', deque(['F'])))
        self.assertEqual(0, cube_scrambler.count_repeat('U', deque(['D'])))
        self.assertEqual(0, cube_scrambler.count_repeat('U', deque(["U'"])))
        self.assertEqual(0, cube_scrambler.count_repeat('U', deque(['U', 'F'])))
        self.assertEqual(0, cube_scrambler.count_repeat('U', deque(['U', 'U', 'F'])))
        self.assertEqual(0, cube_scrambler.count_repeat('U', deque(['U', 'U', 'U', 'F'])))
        self.assertEqual(1, cube_scrambler.count_repeat('U', deque(['U'])))
        self.assertEqual(1, cube_scrambler.count_repeat('U', deque(['U', 'D'])))
        self.assertEqual(1, cube_scrambler.count_repeat('U', deque(['U', "D'"])))
        self.assertEqual(1, cube_scrambler.count_repeat('U', deque(['D', 'U'])))
        self.assertEqual(1, cube_scrambler.count_repeat('U', deque(["D'", 'U'])))
        self.assertEqual(2, cube_scrambler.count_repeat('U', deque(['U', 'U'])))
        self.assertEqual(2, cube_scrambler.count_repeat('U', deque(['U', 'U', 'D'])))
        self.assertEqual(2, cube_scrambler.count_repeat('U', deque(['U', 'D', 'U'])))
        self.assertEqual(2, cube_scrambler.count_repeat('U', deque(['U', 'U', "D'"])))
        self.assertEqual(2, cube_scrambler.count_repeat('U', deque(['U', "D'", 'U'])))
        self.assertEqual(2, cube_scrambler.count_repeat('U', deque(['D', 'U', 'U'])))
        self.assertEqual(2, cube_scrambler.count_repeat('U', deque(["D'", 'U', 'U'])))

    def test_contains_opposite(self):
        self.assertTrue(cube_scrambler.contains_opposite('U', deque(["U'"])))
        self.assertTrue(cube_scrambler.contains_opposite('U', deque(["U'", 'D'])))
        self.assertTrue(cube_scrambler.contains_opposite('U', deque(["U'", 'D', 'D'])))
        self.assertFalse(cube_scrambler.contains_opposite('U', deque(['D'])))
        self.assertFalse(cube_scrambler.contains_opposite('U', deque(['F'])))
        self.assertFalse(cube_scrambler.contains_opposite('U', deque(["U'", 'F'])))
        self.assertFalse(cube_scrambler.contains_opposite('U', deque(["U'", "U'", 'F'])))

    def test_half_turn_suffix(self):
        self.assertEqual('', cube_scrambler.MoveSequence.half_turn_suffix(1))
        self.assertEqual('2', cube_scrambler.MoveSequence.half_turn_suffix(2))
        self.assertEqual("'", cube_scrambler.MoveSequence.half_turn_suffix(3))
        with self.assertRaises(ValueError):
            cube_scrambler.MoveSequence.half_turn_suffix(0)
            cube_scrambler.MoveSequence.half_turn_suffix(4)
            cube_scrambler.MoveSequence.half_turn_suffix(5)
            cube_scrambler.MoveSequence.half_turn_suffix(-1)

    def test_condensed_chain(self):
        self.assertListEqual(['U'], list(cube_scrambler.MoveSequence.condensed_chain(['U'])))
        self.assertListEqual([], list(cube_scrambler.MoveSequence.condensed_chain(['U', "U'"])))
        self.assertListEqual(['U2'], list(cube_scrambler.MoveSequence.condensed_chain(['U', 'U'])))
        self.assertListEqual(["U'"], list(cube_scrambler.MoveSequence.condensed_chain(['U', 'U', 'U'])))
        self.assertListEqual([], list(cube_scrambler.MoveSequence.condensed_chain(['U', 'U', 'U', 'U'])))
        self.assertListEqual(['B'], list(cube_scrambler.MoveSequence.condensed_chain(['F', 'B', "F'"])))
        self.assertListEqual(['B2'], list(cube_scrambler.MoveSequence.condensed_chain(['F', 'B', "F'", 'B'])))


if __name__ == '__main__':
    unittest.main(exit=False)
