import numpy as np


def word_distance(w1, w2):
    return np.sqrt(2) * np.sqrt(1 - np.dot(w1, w2) / (np.linalg.norm(w1) * np.linalg.norm(w2)))


def calculate_similarity_matrix(w1, w2):
    dist = [[word_distance(a, b) for a in w1] for b in w2]
    return dist


def calculate_word_amplitude(w):
    return np.linalg.norm(w)
