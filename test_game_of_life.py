import io
import sys
import unittest
import game_of_life

class TestGameOfLife(unittest.TestCase):
    def setUp(self):
        self.get_next_gen = game_of_life.get_next_gen
        self.driver = game_of_life.driver
        self.is_grid_size_valid = game_of_life.is_grid_size_valid
        self.is_row_input_valid = game_of_life.is_row_input_valid
        self.print_grid = game_of_life.print_grid
        self.print_generations = game_of_life.print_generations

    def test_is_grid_size_valid_succeeds(self):
        self.assertTrue(self.is_grid_size_valid(10, 20))

    def test_is_grid_size_valid_zero_rows(self):
        self.assertFalse(self.is_grid_size_valid(0, 20))

    def test_is_grid_size_valid_zero_cols(self):
        self.assertFalse(self.is_grid_size_valid(10, 0))

    def test_is_row_input_valid_succeeds(self):
        self.assertTrue(self.is_row_input_valid([1, 0, 0, 1], 4))

    def test_is_row_input_valid_wrong_cols(self):
        self.assertFalse(self.is_row_input_valid([1, 1, 0, 0,1], 4))

    def test_is_row_input_valid_wrong_cells(self):
        self.assertFalse(self.is_row_input_valid([1, 1, 2, 1], 4))

    def test_get_next_gen(self):
        rows = 5
        cols = 8
        initial_grid = [[1, 0, 0, 1, 1, 0, 1, 0], [0, 1, 1, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0, 0], [0, 1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 0, 1, 0, 1, 0]]
        expected_grid = [[1, 0, 0, 0, 1, 0, 0, 1], [0, 0, 1, 1, 1, 1, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 1, 1, 0, 1, 1], [1, 0, 0, 0, 1, 0, 1, 0]]
        self.assertEqual(self.get_next_gen(initial_grid, rows, cols), expected_grid)

    def test_print_grid(self):
        stdout = io.StringIO()
        sys.stdout = stdout
        self.print_grid([[1, 0, 1], [1, 1, 1], [0, 0, 1]])
        sys.stdout = sys.__stdout__
        self.assertRegex(stdout.getvalue(), "101\n111\n001\n")

    def test_print_generations(self):
        stdout = io.StringIO()
        sys.stdout = stdout
        self.print_generations([[1, 0, 1], [0, 0, 0], [0, 0, 1]], 3, 3, 2)
        sys.stdout = sys.__stdout__
        self.assertRegex(stdout.getvalue(), "111\n111\n111\n")
        self.assertRegex(stdout.getvalue(), "000\n000\n000\n")

    def test_driver_throws_invalid_grid_size_exception(self):
        stdin = io.StringIO("0\n0\n")
        sys.stdin = stdin
        self.assertRaisesRegex(ValueError, "Invalid grid size.", self.driver)

    def test_driver_throws_invalid_grid_input_exception(self):
        stdin = io.StringIO("3\n2\n1 0\n2 1")
        sys.stdin = stdin
        self.assertRaisesRegex(ValueError, "Invalid input for the grid.", self.driver)

    def test_driver_prints_correct_initial_grid(self):
        stdin = io.StringIO("3\n2\n1 0\n0 1\n0 0\n2")
        stdout = io.StringIO()
        sys.stdin = stdin
        sys.stdout = stdout
        self.driver()
        sys.stdout = sys.__stdout__
        self.assertRegex(stdout.getvalue(), "Initial grid: \n10\n01\n00\n")

if __name__ == '__main__':
    unittest.main()