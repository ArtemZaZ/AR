import numpy as np


def normalize(vec):     # приведение массива к нормали
    norm = np.linalg.norm(vec)
    if norm:
        return vec / norm
    else:
        return vec
