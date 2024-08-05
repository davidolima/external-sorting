from typing import List
from utils import generate_sequences_to_tests
from heap import Heap
from p_ways import PWays

from tqdm import tqdm
import random 

main_memory_size:int = 5
max_num_sorted_sequences:int = 1000
max_open_files:int = 4

for i in tqdm(range(1, max_num_sorted_sequences)):
    num_sorted_sequences: int = i+1
    dummy_num_sorted_sequences:int = num_sorted_sequences * 2
    sequences:List[int] = []
    num_sequences:int = 0

    while True:
        sequences = generate_sequences_to_tests(main_memory_size, dummy_num_sorted_sequences, max_value=100*num_sorted_sequences)
        heap = Heap(main_memory_size, sequences)
        sorted_sequences = heap.sort()
        num_sequences = len(sorted_sequences)

        if num_sequences >= num_sorted_sequences:
            sorted_sequences = sorted_sequences[:num_sorted_sequences]
            index = 0
            for sequence in sorted_sequences:
                index += len(sequence)

            break

    #print(f"Tesde Nº {i} de  {max_num_sorted_sequences}")
    p_ways = PWays(main_memory_size, sequences[:index], num_sorted_sequences, max_open_files, save_results=True, print_results=False)
    p_ways.sort()
    #print()
    