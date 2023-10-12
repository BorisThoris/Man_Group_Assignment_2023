## This document serves as a statistical defence of `RandomGen`, confirming its consistent and reliable performance.

**Testing Details:**

- **Scope:** Conducted across `10,000` variations with each running `10,000` times, totaling `100,000,000` (*one hundred million*) runs.
  
- **Procedure:** 
  - Each variation generates random numbers (range: `-1,000,000,000` to `1,000,000,000`).
  - Determines random probabilities, ensuring their sum equals `1`.
  - Calls `RandomGen` function `10,000` times per variation.
  - Compares the count of each number's occurrence to its expected count based on given probabilities.
  
- **Tolerance:** Allows a `2%` variance.

**Results:**
`RandomGen` function passed  all tests with `0` Assertions, adhering to defined probabilities within a `2%` tolerance.


## This test is slow but can be made to run less time, however: Due to the inherent unpredictability of random probabilities, this test shouldn't be included in the code, as there's never a 100% that it won't fail.


**Test used:**
```python
     def test_random_gen(self):
        test_count = 0

        max_amount_of_numbers = RandomGen._MAX_LIST_LENGTH
        max_number = RandomGen._MAX_ALLOWED_INT

        for _ in range(10000):
            test_count += 1  # Increment the test count for each iteration

            # 1. Generate random probabilities and numbers that adhere to the rules.
            num_numbers = randint(1, max_amount_of_numbers)
            numbers = sample(range(-max_number, max_number), num_numbers)  # Random numbers within the allowed range.
            random_probabilities = [random() for _ in range(num_numbers)]
            total_prob = sum(random_probabilities)
            probabilities = [prob / total_prob for prob in random_probabilities]  # Normalize to make sum equal to 1.

            # 2. Initialize a `RandomGen` instance with these numbers and probabilities.
            random_gen = RandomGen(numbers, probabilities)

            # 3. Run the `next_num` function 10,000 times and record the output each time.
            num_trials = 10000
            results = defaultdict(int)
            for _ in range(num_trials):
                result = random_gen.next_num()
                results[result] += 1

            # 4. Compare the frequency of each number to its expected frequency based on its probability.
            for number, prob in zip(numbers, probabilities):
                expected_count = prob * num_trials
                actual_count = results[number]
                tolerance = 0.02 * num_trials  # 2% tolerance

                if actual_count > 20:
                    print()
                    print("nearing tolerance")
                    print("tolerance")
                    print(expected_count + tolerance)
                    print("actual_count")
                    print(actual_count)
                    print()

                assert expected_count - tolerance <= actual_count <= expected_count + tolerance, \
                    f"Test {test_count}: Number {number} was expected to appear about {expected_count} times but appeared {actual_count} times."
```

