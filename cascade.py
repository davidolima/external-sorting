#!/usr/bin/env python3

from math import inf
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
            num_sorted_sequences=0, # <--- Não faz nada
            max_open_files=max_open_files
        )

        self.registers = registers
        self.main_memory_size = main_memory_size # TODO: Move to polyphasic.
        self._files = [[] for _ in range(max_open_files)]
        self._fase = 0

        self._get_sorted_sequences()


    @staticmethod
    def _calculate_ideal_previous_line(line: List[int]) -> List[int]:
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
        return curr_line

    def _get_sorted_sequences(self) -> None:
        initial_seqs = Heap(
            main_memory_size=self.main_memory_size,
            registers=self.registers.copy(),
        ).sort()

        ideal_sizes: List[int] = Cascade._get_ideal_initial_seq_sizes(
            n_seqs=len(self.registers),
            max_open_files=self.max_open_files
        )

        for i in range(len(initial_seqs)):
            file_idx = i%(self.max_open_files-1) # Distribuir as seq. ord. nos arquivos de input
            self._files[file_idx].extend(initial_seqs[i])
            self._files[file_idx] = sorted(self._files[file_idx])
            if len(self._files[file_idx]) < ideal_sizes[file_idx]:
                diff = [-1]*(ideal_sizes[file_idx]-len(self._files))
                self._files[file_idx].extend(diff)

        for i in range(len(self._files)):
            self._files[i] = [[x] for x in self._files[i]]

        self._out_idx = self._files.index([])
        self._print_fase()

    def _get_sorted_sequences_(self) -> None:
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
            if len(self._files[file_idx]) < ideal_sizes[file_idx]:
                diff = [[-1]]*(len(self._files) - ideal_sizes[file_idx])
                self._files[file_idx].extend(diff)

        self._out_idx = self._files.index([])
        self._print_fase()

    def _print_fase(self):
        """
        Imprime o estado da fase atual na notação pedida.
        """
        stringify = lambda s: str(s)[1:-1].replace('[','{').replace(']','}').replace(',', '')
        print(f"fase {self._fase} {self.calculate_avg_seq_size()}")
        [print(str(i+1)+":", stringify(s)) for i, s in enumerate(self._files)]
        self._fase+=1

    def calculate_avg_seq_size(self):
        print("WARNING: `Cascate.calculate_avg_seq_size` has not been implemented yet.")
        return 0

    def _get_smallest_seq(self) -> list:
        min = self._files[0]
        for file in self._files:
            if file and len(min) > len(file):
                min = file
        return min

    def _qtd_seqs(self) -> int:
        return sum([len(file) for file in self._files])

    def _qtd_registros(self) -> int:
        qtd = 0
        for file in self._files:
            qtd += sum([len(seq) for seq in file])
        return qtd

    def _get_input_files(self):
        input_files = self._files.copy()
        input_files.remove([])
        return input_files

    def merge_files(self, file_idxs: list[int]) -> list[int]:
        sequences = [self._files[i] for i in file_idxs]
        indices = [0] * len(sequences)
        out = []

        while len(self._get_smallest_seq()) > 0:
            # Lista com o menor (primeiro) elemento de cada sequência.
            # Além disso, substitui todos os índices OOB por `inf`
            current_elements: list[int] = [sequences[i][indices[i]] if indices[i] >= 0 else inf for i in range(len(indices))]
            print(current_elements, out)
            #print(sequences)

            min_element = min(current_elements)
            min_element_idx: int = current_elements.index(min_element)

            out += current_elements[min_element_idx]
            sequences[min_element_idx].remove(min_element)
            indices[min_element_idx] += 1
            if indices[min_element_idx] >= len(sequences[min_element_idx]):
                indices[min_element_idx] = -1

        return out

    def sort(self) -> List[List[int]]:
        while len(self._get_smallest_seq()) > 0:
            out_idx = self._files.index([])
            to_merge = list(range(self.max_open_files))
            to_merge.pop(out_idx)
            merged = self.merge_files(to_merge)
            self._files[out_idx].append(merged)
            self._print_fase()

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
    cascade = Cascade(
        registers            = [18, 7, 3, 24, 15, 5, 20, 25, 16, 14, 21, 19, 1, 4, 13, 9, 22, 11, 23, 8, 17, 6, 12, 2, 10], #[random.randint(1, 100) for _ in range(args.n_registers)],
        max_open_files       = args.max_open_files,
        initial_seq_size     = args.initial_seq_size,
        main_memory_size     = args.main_memory_size,
    )
    cascade.sort()
    print("--- End Result --------------")
    #cascade._print_fase()
