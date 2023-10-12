# Algorithms Coding Assignment

**Content**
- [Objective](#objective)
- [Usage Example](#usage-example)
- [Class Overview](#class-overview)
    - [Attributes](#attributes)
    - [Error Messages](#error-messages)
    - [Methods](#methods)
- [Statistical Defence](#statistical-defence)
- [Unit Tests Suite](#unit-tests-suite)


---

## Objective
Create a class `RandomGen` that can generate random numbers from a list based on specified probabilities. Also, implement the `next_num()` method and accompanying unit tests.


## Usage Example
```python
numbers = [-1, 0, 1, 2, 3]
probabilities = [0.01, 0.3, 0.58, 0.1, 0.01]
random_gen = RandomGen(numbers, probabilities)
print(random_gen.next_num())  # Outputs a random number based on given probabilities.
```

---

## Class Overview

#### Attributes
- **_PROB_TOTAL (float)**: Expected total for the probabilities (1.0).
- **_ROUND_PRECISION (int)**: Rounding precision for floating-point probabilities (2).
- **_MAX_ALLOWED_INT (int)**: Maximum allowed integer (10^9).
- **_MAX_LIST_LENGTH (int)**: Maximum list length (1000).

#### Error Messages
Various error messages are defined as class attributes to handle various input discrepancies:
- Mismatched list lengths.
- Non-integer values in the numbers list.
- Non-float values or negative probabilities.
- Incorrect probability totals.
- Numbers exceeding the maximum allowed value.

#### Methods
- **__init__(self, numbers, probabilities)**: Initializes with provided numbers and probabilities. Performs various data integrity checks.
  
- **next_num(self)**: Returns a random number from the numbers list, based on the associated probabilities.
  
- **_validate_input_lengths**, **_validate_number**, **_validate_probability**, **_validate_probability_total**: These methods ensure that the input adheres to specified requirements.
  
- **_process_entries_and_merge_duplicates**: Processes and merges any duplicate numbers by summing their probabilities.
  
- **_compute_cumulative_probabilities**: Calculates the cumulative probabilities.
  
- **_find_insert_position**: Binary search function used to swiftly find the suitable interval for a generated random probability.

---

## Statistical Defence 
- can be found in Statistical_Defense_ReadMe.md 

## Unit Tests Suite
1. **Initialization and validation tests**: These tests check the robustness of the class initialization procedure.
   - **Length mismatch**: Verifies that the class raises an error if the number of elements in the numbers list doesn't match the probabilities list.
   - **Random numbers type-check**: Ensures that only integers are accepted as valid numbers.
   - **Probabilities type-check**: Checks that only floats are accepted for probabilities.
   - **Negative probability**: Validates that the class rejects negative probabilities.
   - **Probabilities sum validation**: Ensures that the total of all probabilities is exactly 1.
   - **Empty list validation**: Checks if the class raises an error when provided with empty lists.
   - **List length validation**: Ensures the class raises an error if the list lengths exceed the defined maximum.
   - **Number size validation**: Confirms that only numbers within the permitted range are accepted.
   
2. **`next_num` method tests**: These tests validate the core functionality of generating numbers based on their associated probabilities.
   - **Basic input check**: Verifies the method's output with simple, non-duplicate values.
   - **Handling duplicates**: Confirms that the method correctly processes and returns numbers even when there are duplicates in the numbers list.
   - **Single input test**: Checks the behavior of the class when only one number and its probability are provided.
   - **Non-adjacent duplicates**: Validates the method's response when there are non-consecutive duplicate numbers in the list.
   - **List with all duplicates**: Checks the method's behavior when every number in the list is identical.
   - **Zero probabilities**: Ensures that the method can handle and return numbers even when some of them have a zero probability.

