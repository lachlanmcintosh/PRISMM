import numpy as np
import sys

# m[i,j] tells you the probability of going from copy number i to copy number j in 1 generation
# m[i,j]^k tells you the probability of going from copy number i to copy number j in k generations

path_length = int(sys.argv[1])
u = float(sys.argv[2])
d = float(sys.argv[3])

dimension = 1 + 2 ** path_length
m = np.zeros((dimension, dimension))

# base case
m[0, 0] = 1
m[1, 0] = d
m[1, 1] = 1 - u - d
m[1, 2] = u

# other cases
for i in range(2, 2 ** (path_length-1) + 1):
    print(i)
    for j in range(dimension):  # This ensures you won't go out of bounds
        u_term = m[i-1, j-2] * u if j-2 >= 0 else 0
        neutral_term = m[i-1, j-1] * (1 - u - d) if j-1 >= 0 else 0
        d_term = m[i-1, j] * d
        m[i, j] = u_term + neutral_term + d_term

    print(m[i, :])

# Print the resulting matrix
print(m)

