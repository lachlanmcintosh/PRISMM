import numpy as np
import sys

# Extracted code to generate the genome doubling Markov matrix G
path_length = int(sys.argv[1])  # Assuming path_length is passed as a command-line argument
dimension =  1+2**(path_length)
G = matrix(QQ, dimension, dimension, 0)  # Create a zero matrix of the appropriate size

for i in range(round(dimension/2)):
    G[i, 2*i] = 1

# Save G to an .sobj file
save(G, 'MATRICES/p'+str(path_length)+'_v5/GD.sobj')
