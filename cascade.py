#!/usr/bin/env python3

from typing import *
from polyphasic import Polyphasic
from heap import Heap

class Cascade(Polyphasic):
    def __init__(
        self,
        registers: List[int],
        initial_seq_size: int,
        max_open_files: int,
        main_memory_size:int,
    ) -> None:
        super().__init__(
            registers=registers,
            initial_seq_size=initial_seq_size,
            max_open_files=max_open_files
        )

        self.main_memory_size = main_memory_size # TODO: Move to polyphasic.
        self._files = [[] for _ in range(max_open_files)]
        self._fase = 0

        self._get_sorted_sequences()

    def _get_sorted_sequences(self) -> None:
        initial_seqs = Heap(
            main_memory_size=self.main_memory_size,
            registers=self.registers,
        ).sort()

        ideal_sizes: List[int] = Cascade._get_ideal_initial_seq_sizes(
            n_seqs=len(self.registers),
            max_open_files=self.max_open_files
        )

        for i in range(len(initial_seqs)):
            file_idx = i%(self.max_open_files-1) # Distribuir as seq. ord. nos arquivos de input
            self._files[file_idx].append(initial_seqs[i])

        self._out_idx = Polyphasic.indice_lista_vazia(self._files)
        self._print_fase()

    @staticmethod
    def _calculate_ideal_previous_line(line: List[int]):
        r = [0]*len(line)
        curr_line = line.copy()
        # Weird way of doing it, but just to move the empty file around
        valid_idxs = list(range(len(line)))
        valid_idxs.remove(line.index(max(line)))
        for i in valid_idxs:
            curr_line.remove(min(curr_line))
            r[i] = sum(curr_line)
        return r
    
    @staticmethod
    def _get_ideal_initial_seq_sizes(n_seqs: int, max_open_files: int) -> List[int]:
        curr_line = [0] * max_open_files
        curr_line[-1] = 1
        while (sum(curr_line) < n_seqs):
            curr_line = Cascade._calculate_ideal_previous_line(curr_line)
        print(curr_line, sum(curr_line))
        return curr_line

    def _print_fase(self):
        print(f"fase {self._fase} {self.calculate_avg_seq_size()}")
        [print(str(i+1)+":", str(s)[1:-1].replace('[','{').replace(']','}')) for i, s in enumerate(self._files)]
        self._fase+=1

    def calculate_avg_seq_size(self):
        print("WARN: Not implemented yet.")
        return 0

    def _qtd_registros(self):
        qtd = 0
        for file in self._files:
            qtd += sum([len(seq) for seq in file])
        return qtd

    def sort(self) -> List[List[int]]:
        sequences_to_merge = self._files.copy()
        out_idx = Polyphasic.indice_lista_vazia(self._files)
        sequences_to_merge.pop(out_idx)
        # Pegar a primeira sequência de cada arquivo.
        sequences_to_merge = [x[-1] for x in sequences_to_merge]
        for i, x in enumerate(sequences_to_merge):
            print(x, "qtd regs:", self._qtd_registros())
            self._files[i].remove(x)
            self._files[out_idx].append(Polyphasic.merge_n_lists(sequences_to_merge))
            #out_idx -= 1
        return self._files

if __name__ == "__main__":
    import random
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(prog="Cascade Merge Sort", description="Por David Lima, Israel Pedreira e Márcio do Santos")
    parser.add_argument("-n", "--n_registers",      default=25)
    parser.add_argument("-p", "--max_open_files",   default=5)
    parser.add_argument("--initial_seq_size",       default=1)
    parser.add_argument("-m", "--main_memory_size", default=3)
    args = parser.parse_args()

    # Run algorithm
    sorted = Cascade(
        registers            = [18, 7, 3, 24, 15, 5, 20, 25, 16, 14, 21, 19, 1, 4, 13, 9, 22, 11, 23, 8, 17, 6, 12, 2, 10], #[random.randint(1, 100) for _ in range(args.n_registers)],
        max_open_files       = args.max_open_files,
        initial_seq_size     = args.initial_seq_size,
        main_memory_size     = args.main_memory_size,
    ).sort()
    print("--- End Result --------------")
    [print(i) for i in sorted]
