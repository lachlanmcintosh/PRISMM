import numpy as np
import unittest
from simulate_data import compute_transition_matrix, generate_observations

class TestSimulation(unittest.TestCase):

    def test_row_sums(self):
        transition_matrix = compute_transition_matrix([1, 1, 1, 1, 0], 10, model=2)
        print("Transition matrix in test_row_sums:")
        print(transition_matrix)
        observations = generate_observations(transition_matrix, 1, 100)  # Adding this line
        print("Generated observations:")
        print(observations)
        row_sums = np.sum(transition_matrix, axis=1)
        print("Row sums:")
        print(row_sums)
        np.testing.assert_almost_equal(row_sums, np.ones(transition_matrix.shape[0]))

    def test_shape_transition_matrix(self):
        transition_matrix = compute_transition_matrix([1, 1, 1], 5, model=0)
        print("Transition matrix in test_shape_transition_matrix:")
        print(transition_matrix)
        observations = generate_observations(transition_matrix, 1, 100)  # Adding this line
        print("Generated observations:")
        print(observations)
        self.assertEqual(transition_matrix.shape, (5, 5))

    def test_shape_observations(self):
        transition_matrix = compute_transition_matrix([1, 1, 1], 5, model=0)
        observations = generate_observations(transition_matrix, 1, 100)
        print("Transition matrix in test_shape_observations:")
        print(transition_matrix)
        print("Generated observations:")
        print(observations)
        self.assertEqual(len(observations), 5)

    def test_non_negative_observations(self):
        transition_matrix = compute_transition_matrix([0.1, 0.4, 1, 0], 20, model=1)
        print("Transition matrix in test_non_negative_observations:")
        print(transition_matrix)
        observations = generate_observations(transition_matrix, 1, 100)  # Adding this line
        print("Generated observations:")
        print(observations)
        self.assertTrue(all(obs >= 0 for obs in observations))

    def test_sum_observations(self):
        transition_matrix = compute_transition_matrix([1, 1, 1, 1, 1], 5, model=2)
        print("Transition matrix in test_sum_observations:")
        print(transition_matrix)
        observations = generate_observations(transition_matrix, 1, 100)  # Adding this line
        print("Generated observations:")
        print(observations)
        self.assertEqual(np.sum(observations), 100)

    def test_state_transitions(self):
        transition_matrix = compute_transition_matrix([0.2, 1, 1], 10, model=0)
        print("Transition matrix in test_state_transitions:")
        print(transition_matrix)
        observations = generate_observations(transition_matrix, 1, 100)  # Adding this line
        print("Generated observations:")
        print(observations)
        self.assertTrue(np.all((0 <= transition_matrix) & (transition_matrix <= 1)))

if __name__ == '__main__':
    unittest.main()
