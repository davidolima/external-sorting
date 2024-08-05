from typing import List
from utils import generate_sequences_to_tests
from heap import Heap
from p_ways import PWays

from tqdm import tqdm
import random 

main_memory_size:int = 5
num_sorted_sequences:int = 5
max_open_files:int = 4

MAX_INT_VALUE = 100
MAX_SEQ_LEN = 10

def generate_sequences(main_memory_size:int, max_value:int, max_seq_len:int, num_sorted_sequences:int) -> List[List[int]]:
    return [[random.randint(0,max_value) for _ in range(random.randint(main_memory_size, max_seq_len))] for _ in range(num_sorted_sequences)]

seqs = generate_sequences(main_memory_size, MAX_INT_VALUE, MAX_SEQ_LEN, num_sorted_sequences)

registers = sum(seqs, [])
print(registers)
quit()

[print(len(x)) for x in seqs]
print("tam total:", len(seqs))
print(seqs)