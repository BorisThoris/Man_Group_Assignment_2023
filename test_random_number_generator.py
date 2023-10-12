import unittest
from unittest.mock import patch
from random_number_generator import RandomGen


class TestRandomGen(unittest.TestCase):

    # Initialization and validation tests
    def test_length_mismatch(self):
        """Test if a ValueError is raised when the number of numbers does not match the number of probabilities."""
        with self.assertRaises(ValueError) as context:
            RandomGen([1, 2, 3], [0.4, 0.6])
        self.assertEqual(str(context.exception),
                         RandomGen._ERR_LENGTH_MISMATCH.format(numbers_len=3, probabilities_len=2))

    def test_random_numbers_not_int(self):
        """Test if a ValueError is raised when provided numbers are not integers."""
        with self.assertRaises(ValueError) as context:
            RandomGen([1.5, 2], [0.5, 0.5])
        self.assertEqual(str(context.exception), RandomGen._ERR_NUMBERS_INT.format(num=1.5, num_type='float'))

    def test_probabilities_not_float(self):
        """Test if a ValueError is raised when provided probabilities are not floats."""
        with self.assertRaises(ValueError) as context:
            RandomGen([1, 2], [0.5, "0.5"])
        self.assertEqual(str(context.exception), RandomGen._ERR_PROBABILITIES_FLOAT.format(prob="0.5", prob_type='str'))

    def test_negative_probability(self):
        """Test if a ValueError is raised when negative probability is provided."""
        with self.assertRaises(ValueError) as context:
            RandomGen([1, 2], [0.5, -0.5])
        self.assertEqual(str(context.exception), RandomGen._ERR_NEGATIVE_PROB.format(prob=-0.5))

    def test_probabilities_sum_invalid(self):
        """Test if a ValueError is raised when the sum of probabilities is not 1."""
        with self.assertRaises(ValueError) as context:
            RandomGen([1, 2], [0.5, 0.6])
        self.assertEqual(str(context.exception), RandomGen._ERR_PROB_SUM_INVALID.format(total_prob=1.1))
        with self.assertRaises(ValueError) as context:
            RandomGen([1, 2], [0.1, 0.1])
        self.assertEqual(str(context.exception), RandomGen._ERR_PROB_SUM_INVALID.format(total_prob=0.2))

    def test_empty_lists(self):
        """Test if a ValueError is raised when empty lists are provided."""
        for nums, probs in [([], []), ([1, 2, 3], []), ([], [0.3, 0.3, 0.4])]:
            with self.assertRaises(ValueError) as context:
                RandomGen(nums, probs)
            self.assertEqual(str(context.exception), RandomGen._ERR_EMPTY_LIST)

    def test_exceed_max_list_length(self):
        """Test if a ValueError is raised when the number of elements exceeds the maximum allowed length."""
        with self.assertRaises(ValueError) as context:
            RandomGen([1] * (RandomGen._MAX_LIST_LENGTH + 1), [0.001] * (RandomGen._MAX_LIST_LENGTH + 1))
        self.assertEqual(str(context.exception), RandomGen._ERR_LIST_TOO_LONG.format(RandomGen._MAX_LIST_LENGTH))

    def test_numbers_exceed_max_allowed_int(self):
        """Test if a ValueError is raised when a number in the list exceeds the maximum allowed integer."""
        with self.assertRaises(ValueError) as context:
            RandomGen([RandomGen._MAX_ALLOWED_INT + 1], [1])
        self.assertEqual(str(context.exception),
                         RandomGen._ERR_NUMBERS_TOO_LARGE.format(num=RandomGen._MAX_ALLOWED_INT + 1,
                                                                 max_int=RandomGen._MAX_ALLOWED_INT)
                         )

    def test_negative_number_exceed_max_allowed_int(self):
        """Test if a ValueError is raised when a negative number in the list exceeds the maximum allowed negative
        integer."""
        with self.assertRaises(ValueError) as context:
            RandomGen([-RandomGen._MAX_ALLOWED_INT - 1], [1])
        self.assertEqual(str(context.exception),
                         RandomGen._ERR_NUMBERS_TOO_LARGE.format(num=-RandomGen._MAX_ALLOWED_INT - 1,
                                                                 max_int=RandomGen._MAX_ALLOWED_INT)
                         )

    def test_compute_cumulative_probabilities(self):
        """Test if cumulative probabilities are computed correctly."""
        random_gen = RandomGen([1, 2, 3], [0.3, 0.3, 0.4])
        self.assertEqual(random_gen._cumulative_probabilities, [0.3, 0.6, 1.0])

    # next_num method tests
    def test_next_num_with_basic_input(self):
        """Test next_num method with basic input."""
        random_numbers = [1, 2, 3]
        probabilities = [0.3, 0.3, 0.4]
        random_gen = RandomGen(random_numbers, probabilities)
        with patch('random_number_generator.random.random') as mock_random:
            mock_random.return_value = 0.35
            self.assertEqual(random_gen.next_num(), 2)
            mock_random.return_value = 0.95
            self.assertEqual(random_gen.next_num(), 3)
            mock_random.return_value = 0.2
            self.assertEqual(random_gen.next_num(), 1)

    def test_next_num_with_duplicate_numbers(self):
        """Test next_num method when numbers contain duplicates."""
        random_numbers = [1, 2, 2, 3]
        probabilities = [0.1, 0.2, 0.3, 0.4]
        random_gen = RandomGen(random_numbers, probabilities)
        with patch('random_number_generator.random.random') as mock_random:
            mock_random.return_value = 0.35
            self.assertEqual(random_gen.next_num(), 2)
            mock_random.return_value = 0.8
            self.assertEqual(random_gen.next_num(), 3)
            mock_random.return_value = 0.05
            self.assertEqual(random_gen.next_num(), 1)

    def test_single_number_and_probability(self):
        random_gen = RandomGen([5], [1.0])
        with patch('random_number_generator.random.random') as mock_random:
            mock_random.return_value = 0.5
            self.assertEqual(random_gen.next_num(), 5)

    def test_non_adjacent_duplicates(self):
        random_numbers = [1, 2, 3, 2, 4, 2]
        probabilities = [0.1, 0.2, 0.1, 0.2, 0.1, 0.3]
        random_gen = RandomGen(random_numbers, probabilities)
        with patch('random_number_generator.random.random') as mock_random:
            mock_random.return_value = 0.7
            self.assertEqual(random_gen.next_num(), 2)

    def test_only_duplicates(self):
        random_numbers = [1, 1, 1, 1, 1, 1]
        probabilities = [0.1, 0.2, 0.1, 0.2, 0.1, 0.3]
        random_gen = RandomGen(random_numbers, probabilities)
        with patch('random_number_generator.random.random') as mock_random:
            mock_random.return_value = 0.7
            self.assertEqual(random_gen.next_num(), 1)

    def test_zero_probabilities(self):
        random_numbers = [1, 2, 3]
        probabilities = [0.0, 0.5, 0.5]
        random_gen = RandomGen(random_numbers, probabilities)
        with patch('random_number_generator.random.random') as mock_random:
            mock_random.return_value = 0.3
            self.assertEqual(random_gen.next_num(), 2)


if __name__ == "__main__":
    unittest.main()
