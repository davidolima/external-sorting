from typing import List
from utils import generate_sequences_to_tests
from heap import Heap

import random

main_memory_size:int = 3
num_sorted_sequences:int = 100

sequences:List[int] = generate_sequences_to_tests(main_memory_size, num_sorted_sequences, max_value=100*num_sorted_sequences)

heap = Heap(main_memory_size, sequences)
sorted = heap.sort()
print(len(sorted))