import unittest
import numpy as np
from aneuploidy import aneuploidy
from genome_doubling import genome_doubling

class TestModels(unittest.TestCase):
    def test_row_sums(self):
        A = aneuploidy(50, 1, 1, 2)
        G = genome_doubling(50)

        self.assertTrue(np.allclose(np.sum(A, axis=1), 1, atol=1e-6))
        self.assertTrue(np.allclose(np.sum(G, axis=1), 1, atol=1e-6))



size = 50

# Example 1: aneuploidy first, then genome_doubling
CTMC_anueploidy_first = np.dot(aneuploidy(size, 1, 1, 2), genome_doubling(size))
row_sums_anueploidy_first = np.sum(CTMC_anueploidy_first, axis=1)
start = np.zeros(size)
start[1] = 1
new_state_anueploidy_first = np.dot(start, CTMC_anueploidy_first)

# Example 2: genome_doubling first, then aneuploidy
CTMC_genome_doubling_first = np.dot(genome_doubling(size), aneuploidy(size, 1, 1, 2))
row_sums_genome_doubling_first = np.sum(CTMC_genome_doubling_first, axis=1)
new_state_genome_doubling_first = np.dot(start, CTMC_genome_doubling_first)

# Print results
print("\n---------------------------------------------\n")
print("anueploidy matrice:")
A= aneuploidy(size, 1, 1, 2)
print(A)
print(np.sum(A,axis=1))
print("genome doubling matrice")
G=genome_doubling(size)
print(G)
print(np.sum(G,axis=1))
print("\n---------------------------------------------\n")

print("CTMC with anueploidy first:\n", CTMC_anueploidy_first)
print("\nRow sums with anueploidy first:\n", row_sums_anueploidy_first)
print("\nNew state with anueploidy first:\n", new_state_anueploidy_first)

print("\n---------------------------------------------\n")

print("CTMC with genome doubling first:\n", CTMC_genome_doubling_first)
print("\nRow sums with genome doubling first:\n", row_sums_genome_doubling_first)
print("\nNew state with genome doubling first:\n", new_state_genome_doubling_first)
