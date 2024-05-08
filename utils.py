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

def beta(main_memory_size: int, num_sequences_actual_phase:int, generated_sequences_at_actual_phase: Union(List[List[int]], List[List[List[int]]], int)):
    """the generated_sequences_at_actual_phase is a list of files a list of sequences of the actual number of
    registers generated in the actual phase"""

    sum_size_of_generated_sequences = 0
    if type(generated_sequences_at_actual_phase) is int:
        sum_size_of_generated_sequences = generated_sequences_at_actual_phase

    elif type(generated_sequences_at_actual_phase) is List[List[int]]:
        for seq in generated_sequences_at_actual_phase:
            sum_size_of_generated_sequences += len(seq)

    elif type(generated_sequences_at_actual_phase) is List[List[List[int]]]:
        for file in generated_sequences_at_actual_phase:
            for seq in file:
                sum_size_of_generated_sequences += len(seq)

    return (1/(main_memory_size + num_sequences_actual_phase)) * sum_size_of_generated_sequences

def argmin(arr: List[int]) -> int:
    min = inf
    idx = -1

    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i]
            idx = i
    return idx
