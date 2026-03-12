import re
import numpy as np
from collections import defaultdict

def tokenize(text):
    # Remove everything that isn't a letter or space, lower case everything, and split them into separate words
    return re.sub(r'[^a-z\s]', '', text.lower()).split()

def build_matrix(words):
    vocab = list(set(words)) # List of unique words
    idx = {} 
    for i, w in enumerate(vocab):
        idx[w] = i # Gives each word an index starting from 0
    n = len(vocab) # Number of unique words

    counts = np.zeros((n, n)) # Zero n x n matrix

    # Count how often j follows i
    for i in range(len(words) - 1):
        counts[idx[words[i]]][idx[words[i+1]]] += 1

    # Divide each row by its sum so each row adds to 1
    # In other words, calculate the probabilities
    sums = counts.sum(axis=1, keepdims=True) # Adds up each row of the matrix
    sums[sums == 0] = 1 # Avoid division by 0
    return counts / sums, vocab, idx

def steady_state(matrix):
    # Raise matrix to the 100th power to find the steady state distribution
    converged = np.linalg.matrix_power(matrix, 100)
    return converged[0] # Rows converge, just return the first row but any works

def generate(matrix, vocab, idx, seed=None, length=20):
    # Use the starting word, or just take the first word in vocab
    current = seed if seed in idx else vocab[0]
    words = [current]
    for _ in range(length - 1):
        probs = matrix[idx[current]] # Grab probability row for current word
        current = np.random.choice(vocab, p=probs) # Sample words based on probability
        words.append(current)
    return ' '.join(words)

# Run
print("Paste text, type END when done:\n")
lines = []
while (line := input()) != "END": # Keep reading lines until the word "END" appears
    lines.append(line)

words = tokenize('\n'.join(lines)) # Clean up lines from the raw input
matrix, vocab, idx = build_matrix(words) # Build transition probability matrix

# Steady state matrix
ss = steady_state(matrix)
top5 = sorted(zip(vocab, ss), key=lambda x: -x[1])[:5] # Sort steady state matrix by probability, take top 5
print("\nTop 5 steady-state words:", [w for w, _ in top5])

# Generate
print("\nSeed word (or Enter for random), 'quit' to exit:\n")
while True:
    seed = input("> ").strip()
    if seed == 'quit':
        break
    print(generate(matrix, vocab, idx, seed or vocab[0]))