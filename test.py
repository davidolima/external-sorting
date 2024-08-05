from typing import List
from utils import generate_sequences_to_tests
from heap import Heap

import random

main_memory_size:int = 3
num_sorted_sequences:int = 5

MAX_POSSIBLE_INT = 1000
RANDOM_RANGE = 10

n = random.randint(MAX_POSSIBLE_INT//2, MAX_POSSIBLE_INT)


for i in range(num_sorted_sequences):
    

# sequences = [n]
# for i in range(1,num_sorted_sequences+1):
#     #possible = list(range(n-main_memory_size*i, n-main_memory_size*(i+1),-1))

#     for _ in range(main_memory_size):
#         sequences.append(random.randint(sequences[-1]-RANDOM_RANGE,sequences[-1]))

# deterministico
#sequences = list(range(num_sorted_sequences*main_memory_size**2, 0, -main_memory_size))
print("sequences:", sequences)
heap = Heap(main_memory_size, sequences)

result = heap.sort()
for sequence in result:
    print(sequence)

print(f" -> {len(result)} sequences.")