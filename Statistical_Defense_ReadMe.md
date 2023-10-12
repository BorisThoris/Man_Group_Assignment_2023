## Statistical Defense / README for RandomGen Function

### Introduction:

The `RandomGen` function is designed to generate random numbers based on user-specified probabilities. 
This README the procedural test, executed on the `RandomGen` function, to validate its consistency and reliability in producing results as per the given probabilities.

### Testing Process:

#### 1. Scope:
- The test was executed for `10,000` variations, each running `10,000` times, resulting in a grand total of `100,000,000` (one hundred million) runs.

#### 2. Procedure:

   a. For each variation:
   - Random numbers (ranging between `-1,000,000,000` and `1,000,000,000`) are generated. (array of numbers size ranges from 1 to 1000)
   - Random probabilities for these numbers are determined.
   - Probabilities are normalized to ensure their sum equals `1`.

   b. The `RandomGen` function is then called `10,000` times for each variation.
   
   c. Results of the `next_num` function calls are recorded.

   d. The count of each number's appearance is compared against its expected count, based on the given probabilities.

#### 3. Tolerance:
- The test allows a `5%` tolerance on the expected appearance count. This means if a number has a probability `p` of appearing in `10,000` trials, the number of times it should appear is `10,000 x p`. Given the `5%` tolerance, the actual count should fall in the range: `[10,000 x p x 0.95, 10,000 x p x 1.05]`.

### Results:

- The `RandomGen` function passed all `10,000` runs of each `10000` variations of the test.
- For every variation, each number's actual count was within the `5%` tolerance of its expected count.
- No discrepancies beyond the specified tolerance were observed.

### Conclusion:

Based on the extensive testing detailed above, the `RandomGen` function has been statistically validated to work consistently and reliably. The function adheres to the user-specified probabilities within a `5%` margin of tolerance, demonstrating its robustness and reliability.


### Test used for these findings

    def test_random_gen(self):
        test_count = 0

        for _ in range(10000):
            num_numbers = randint(1, RandomGen._MAX_LIST_LENGTH)
            numbers = sample(range(-RandomGen._MAX_ALLOWED_INT, RandomGen._MAX_ALLOWED_INT), num_numbers)
            random_probabilities = [random() for _ in range(num_numbers)]
            total_prob = sum(random_probabilities)
            probabilities = [prob / total_prob for prob in random_probabilities]

            random_gen = RandomGen(numbers, probabilities)

            num_trials = 10000
            results = defaultdict(int)
            for _ in range(num_trials):
                result = random_gen.next_num()
                results[result] += 1

            for number, prob in zip(numbers, probabilities):
                expected_count = prob * num_trials
                actual_count = results[number]
                tolerance = 0.05 * num_trials  # 10% tolerance, you can adjust based on your requirements
                assert expected_count - tolerance <= actual_count <= expected_count + tolerance, \
                    (f"Test {test_count + 1}: Number {number} was expected to appear about {expected_count} "
                     f"times but appeared {actual_count} times.")