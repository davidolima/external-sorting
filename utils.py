from typing import *
from math import inf

def seq_to_notation(seqs: List[List[List[int]]]):
    n_files = len(seqs)
    line = ""
    for i in range(n_files):
        if len(seqs[i]) > 1:
            line += f"({len(seqs[i])},{len(seqs[i][0])}) "
        else:
            line += "(-,-) "
    return line


def argmin(arr: List[int]) -> int:
    min = inf
    idx = -1

    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i]
            idx = i
    return idx
