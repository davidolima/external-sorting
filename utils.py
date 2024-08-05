from typing import *
import random
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

def beta(main_memory_size: int, num_sequences_actual_phase:int, 
         generated_sequences_at_actual_phase: Union[List[List[int]], 
         List[List[List[int]]], int], depth: int = 0) -> float:
    """
        the generated_sequences_at_actual_phase could be a list of files (depth = 2) 
        a list of sequences (depth = 1) of the actual number of
        registers generated in the actual phase (depth = 0)
    """

    sum_size_of_generated_sequences:int = 0
    if depth == 0 and type(generated_sequences_at_actual_phase) == int:
        sum_size_of_generated_sequences = generated_sequences_at_actual_phase

    elif depth == 2 and type(generated_sequences_at_actual_phase) == list:
        for seq in generated_sequences_at_actual_phase:
            sum_size_of_generated_sequences += len(seq)

    elif depth == 3 and type(generated_sequences_at_actual_phase) == list:
        for file in generated_sequences_at_actual_phase:
            for seq in file:
                sum_size_of_generated_sequences += len(seq)
    else:
        raise ValueError("Depth parameter value is wrong or the type of the generated_sequences_at_actual_phase is not correct.")
    
    return (1/(main_memory_size * num_sequences_actual_phase)) * sum_size_of_generated_sequences

def get_random_num(max_val: int = 100) -> int:
    return random.randint(0, max_val)

def get_bigger_num(previous_num: int) -> int:
    return previous_num + random.randint(1, 10)

def get_lower_num(previous_num: int) -> int:
    return max(1, previous_num - random.randint(1, 10))

def generate_sequences_to_tests(main_memory_size: int, num_sorted_sequences: int, max_value:int = 100) -> List[int]:
    sequences: List[int] = []

    for _ in range(num_sorted_sequences):
        current_sequence = []
        current_sequence.append(get_random_num(max_value))
        
        for _ in range(random.randint(0,10)):
            current_sequence.append(get_bigger_num(current_sequence[-1]))
        
        sequences.extend(current_sequence)

        # Add a break between sequences with lower numbers, ensuring no negatives
        for _ in range(main_memory_size):
            sequences.append(get_lower_num(sequences[-1]))


    return sequences


def argmin(arr: List[int]) -> int:
    min = inf
    idx = -1

    for i in range(len(arr)):
        if arr[i] < min:
            min = arr[i]
            idx = i
    return idx
