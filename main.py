import argparse
import random

from p_ways import PWays
from polyphasic import Polyphasic
from cascade import Cascade

if __name__ == "__main__":
    method = input()
    m, k, r, n = map(int, input().split(' '))
    registers = list(map(int, input().split(' ')))
    if len(registers) == 0:
        registers = [random.randint(0,100) for _ in range(n)]

    sorting_algorithm = None

    match(method):
        case 'B':
            algoritmo = PWays(
                main_memory_size=m,
                registers=registers,
                max_open_files=k,
                num_sorted_sequences=r,
            )
        case 'P':
            algoritmo = Polyphasic(
                main_memory_size=m,
                registers=registers,
                max_open_files=k,
                num_sorted_sequences=r,
            )
        case 'C':
            algoritmo = Cascade(
                main_memory_size=m,
                registers=registers,
                max_open_files=k,
                initial_seq_size=1,
            )
        case _:
            raise ValueError(f"O método `{method}` não existe.")

    algoritmo.sort()
