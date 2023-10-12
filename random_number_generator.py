import random
from collections import defaultdict
from typing import List, Tuple


class RandomGen:
    """
    RandomGen: A class to generate random numbers from a list, weighted by specified probabilities.

    Parameters:
    - numbers (List[int]): A list of integers. Each integer must have an absolute value ≤ 10^9.
    - probabilities (List[float]): A list of probabilities corresponding to each integer in the 'numbers' list. The sum of these probabilities must equal 1.0.

    Attributes:
    - _PROB_TOTAL (float): The expected total for the probabilities, set to 1.0.
    - _ROUND_PRECISION (int): The number of decimal places to which probabilities are rounded, to handle floating-point inaccuracies.
    - _MAX_ALLOWED_INT (int): The maximum absolute value allowed for integers in the list, set to 10^9.
    - _MAX_LIST_LENGTH (int): The maximum length allowed for the input lists, set to 1000.

    Limitations:
    1. Only integers with an absolute value ≤ 10^9 are permitted.
    2. The probabilities must be floats and their sum must equal 1.0.
    3. The length of the numbers and probabilities lists cannot exceed 1000.

    Performance:
    - The class utilizes binary search in the 'next_num' method, offering fast look-up times. For larger lists, this significantly boosts efficiency:
      - Regular traversal would have a complexity of O(n).
      - With binary search, the complexity is reduced to O(log n).

    Example:
        numbers = [-1, 0, 1, 2, 3]
        probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
        random_gen = RandomGen(numbers, probabilities)

        # The output will be a random number from 'numbers', selected based on the provided probabilities.
        print(random_gen.next_num())

    Methods:
    - __init__(self, numbers, probabilities): Initializes the RandomGen instance with the provided numbers and probabilities.
    - next_num(self): Returns a random number from the 'numbers' list, selected based on the associated probabilities.

    Note:
    The output of the 'next_num' method is random, hence it can vary with each call.
    """

    _PROB_TOTAL = 1.0
    _ROUND_PRECISION = 2
    _MAX_ALLOWED_INT = 10 ** 9
    _MAX_LIST_LENGTH = 1000

    _ERR_EMPTY_LIST = "Input Error: Both numbers and probabilities cannot be empty."
    _ERR_LENGTH_MISMATCH = ("Input Error: The numbers list has {numbers_len} elements"
                            " while the probabilities list has {probabilities_len} elements. They should match.")
    _ERR_NUMBERS_INT = "Type Error: Expected an integer in the numbers list but found {num} of type {num_type}."
    _ERR_PROBABILITIES_FLOAT = ("Type Error: Expected a float in the probabilities list but found {prob} of type {"
                                "prob_type}.")
    _ERR_NEGATIVE_PROB = "Value Error: Probabilities cannot be negative. Found a negative value: {prob}."
    _ERR_PROB_SUM_INVALID = "Value Error: The sum of probabilities is {total_prob}, but it must be equal to 1.0."
    _ERR_LIST_TOO_LONG = f"Input Error: The length of the list exceeds the maximum allowed length of {_MAX_LIST_LENGTH}."
    _ERR_NUMBERS_TOO_LARGE = "Value Error: Number {num} in the list exceeds the maximum allowed value of {max_int}."

    def __init__(self, numbers: List[int], probabilities: List[float]):
        """
        Initialize the RandomGen instance with numbers and probabilities.

        Args:
            numbers (list[int]): List of numbers.
            probabilities (list[float]): List of probabilities corresponding to the numbers.

        Raises:
            ValueError: If input conditions are not met.
        """
        self._validate_input_lengths(numbers, probabilities)
        self._numbers, self._probabilities = self._process_entries_and_merge_duplicates(numbers, probabilities)
        self._cumulative_probabilities = self._compute_cumulative_probabilities(self._probabilities)

    def next_num(self) -> int:
        """
        Generate a random number based on the defined probabilities.

        The method first generates a random probability. Using binary search on the
        cumulative probabilities, it identifies the interval where this probability falls.

        Returns:
            int: The random number corresponding to the generated probability.
        """
        random_probability = random.random()
        cumulated_probability_index = self._find_insert_position(self._cumulative_probabilities, random_probability)

        return self._numbers[cumulated_probability_index]

    @classmethod
    def _validate_input_lengths(cls, numbers: List[int], probabilities: List[float]):
        """Validate the lengths of input lists."""
        numbers_len, probabilities_len = len(numbers), len(probabilities)

        if not numbers_len or not probabilities_len:
            raise ValueError(cls._ERR_EMPTY_LIST)
        if numbers_len != probabilities_len:
            raise ValueError(
                cls._ERR_LENGTH_MISMATCH.format(numbers_len=numbers_len, probabilities_len=probabilities_len))
        if numbers_len > cls._MAX_LIST_LENGTH:
            raise ValueError(cls._ERR_LIST_TOO_LONG)

    @classmethod
    def _validate_number(cls, num: int):
        """Validate if the number is within allowed limits."""
        if not isinstance(num, int):
            raise ValueError(cls._ERR_NUMBERS_INT.format(num=num, num_type=type(num).__name__))
        if abs(num) > cls._MAX_ALLOWED_INT:
            raise ValueError(cls._ERR_NUMBERS_TOO_LARGE.format(num=num, max_int=cls._MAX_ALLOWED_INT))

    @classmethod
    def _validate_probability(cls, prob: float):
        """Validate if the probability is within allowed limits."""
        if not isinstance(prob, float):
            raise ValueError(cls._ERR_PROBABILITIES_FLOAT.format(prob=prob, prob_type=type(prob).__name__))
        if prob < 0:
            raise ValueError(cls._ERR_NEGATIVE_PROB.format(prob=prob))

    @classmethod
    def _validate_probability_total(cls, total_prob: float):
        """
        Validate that the total probability is equal to the expected value (typically 1).
        """

        if round(total_prob, cls._ROUND_PRECISION) != cls._PROB_TOTAL:
            raise ValueError(cls._ERR_PROB_SUM_INVALID.format(total_prob=total_prob))

    @classmethod
    def _process_entries_and_merge_duplicates(cls, numbers: List[int],
                                              probabilities: List[float]) -> Tuple[List[int], List[float]]:
        """
        Process and validate the contents of numbers and probabilities lists.

        This method validates each number and probability, and if there are duplicate
        numbers, it merges their associated probabilities. For each duplicate number,
        their probabilities are summed up.
        """
        merged_probs = defaultdict(float)
        total_prob = 0.0

        for num, prob in zip(numbers, probabilities):
            cls._validate_number(num)
            cls._validate_probability(prob)

            # Sum the probabilities for duplicate numbers
            merged_probs[num] += prob
            total_prob += prob

        cls._validate_probability_total(total_prob)

        return list(merged_probs.keys()), list(merged_probs.values())

    @classmethod
    def _compute_cumulative_probabilities(cls, probabilities: List[float]) -> List[float]:
        """Compute cumulative probabilities from a list of probabilities."""
        cumulative_sum = 0
        cumulative_list = []

        for prob in probabilities:
            cumulative_sum += prob
            cumulative_list.append(round(cumulative_sum, cls._ROUND_PRECISION))

        return cumulative_list

    @staticmethod
    def _find_insert_position(cumulative_probs: List[float], target_prob: float) -> int:
        """
        Use binary search to find the insert position of `target_prob` in `cumulative_probs`.

        If `target_prob` matches a value in `cumulative_probs`, return the index where it can be
        inserted to maintain sorted order.

        Args:
            cumulative_probs (list[float]): Sorted list of cumulative probabilities.
            target_prob (float): Target probability value to locate.

        Returns:
            int: The index where `target_prob` can be inserted in `cumulative_probs`.
        """
        low, high = 0, len(cumulative_probs) - 1

        while low <= high:
            mid = (low + high) // 2

            if cumulative_probs[mid] == target_prob:
                return mid
            elif cumulative_probs[mid] < target_prob:
                low = mid + 1
            else:
                high = mid - 1

        return low