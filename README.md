# Coding Homework: Algorithms

Welcome to the repository! This coding homework is centered around implementing a method called `nextNum()` and an accompanying set of unit tests. The main idea is to generate a random number from a provided list based on the probabilities given.

## Assignment Description:

**Objective:** Implement the method `nextNum()` and a set of unit tests. While the preferred language for this assignment is Python, Java and other languages are also accepted. Your code should be of the highest quality, ready to be integrated into a production system.

**Example:** Given Random Numbers `[-1, 0, 1, 2, 3]` and Probabilities `[0.01, 0.3, 0.58, 0.1, 0.01]`, upon calling `nextNum()` 100 times, we might get results such as:
```
-1: 1 time
0: 22 times
1: 57 times
2: 20 times
3: 0 times
```
Note: As the results are random, the exact output may vary.

## Solution Overview:

### Class Structure:

A class was constructed based on the provided blueprint. It is designed to accept two arrays: numbers and their corresponding probabilities.

**Parameters:**
- `numbers (List[int])`: A list of integers. Each integer must have an absolute value ≤ 10^9.
- `probabilities (List[float])`: A list of probabilities corresponding to each integer in the 'numbers' list. Their sum should be 1.0.

### Validation:

To ensure the integrity of the inputs:
1. Only integers with an absolute value ≤ 10^9 are allowed to optimize processes and prevent excess memory usage.
2. Probabilities must be in float format and their total must equal 1.0. This ensures the adherence to the basic principles of probability theory.
3. The length of both 'numbers' and 'probabilities' lists should not exceed 1000.

### Method: `next_num()`

Inside the `next_num()` method, a random probability is generated. Based on this random probability and using the principles of probability theory, we determine the appropriate number from the numbers list.

#### Key Principles Used:

- **Sum of Probabilities:** In probability theory, the sum of the probabilities of all possible outcomes in a sample space must be 1. This is a foundational axiom of probability.
- **Cumulative Probabilities:** The cumulative probability gives us the likelihood of an event X being less than or equal to x. It's valuable for determining the probability range for specific events.

#### Performance:

The solution leverages binary search within the `next_num()` method to efficiently locate the appropriate number from the numbers list based on the random probability generated. This approach provides a notable performance advantage:

- Regular traversal would typically operate at a complexity of O(n).
- Using binary search, this complexity is optimized to O(log n), offering faster lookup times, especially for larger lists.

Certainly! Here's a comparative example to illustrate the performance difference:

#### Example:

Let's consider a scenario where we have a list of 1,024 numbers. This number is chosen because it's \(2^{10}\), so it will help visualize the logarithmic benefit.

1. **Regular Traversal (O(n)):**
   
   In the worst-case scenario, where the number we are looking for is at the end of the list or not in the list at all, we would need to check all 1,024 numbers one-by-one.

2. **Binary Search (O(log n)):**

   For a list of 1,024 numbers:
   - First, check the middle number: this divides the list into two halves (512 numbers each).
   - Let's assume our number is in the second half. We then check the middle of this half, further dividing it into two parts of 256 numbers each.
   - If we continue this process, the progression will be: 512 -> 256 -> 128 -> 64 -> 32 -> 16 -> 8 -> 4 -> 2 -> 1.

   In the worst-case scenario, we would only need to check **10 times** to either find the number or determine it's not in the list, compared to the 1,024 checks required for regular traversal.

---

**Thank you for visiting this repository!** We hope this README provides a clear understanding of the problem and the implemented solution.
