from typing import List, Set, Union

import sys
sys.path.append('..')

from utils.heap import Heap
from utils.utils import beta
import math
import os

class PWays:

    def __init__(self, main_memory_size: int, 
                 num_sorted_sequences: int, max_open_files: int, registers: List[int] = [],
                 sorted_sequences: List[List[int]] = [],
                 save_results: bool = False, is_inputing_sorted_sequences: bool = True) -> None:

        self._main_memory_size: int = main_memory_size

        self._num_sorted_sequences: int = num_sorted_sequences
        self._max_open_files: int = max_open_files
        self._files: List[List[List[int]]] = [[] for _ in range(max_open_files)]

        self._num_input_files: int = math.floor(max_open_files / 2)
        self._index_input_files: Set[int] = set()

        self._num_output_files: int = math.ceil(max_open_files / 2)

        # this class can receive the registers list or the heap result (sorted sequences)
        if is_inputing_sorted_sequences:
            self._populate_files(sorted_sequences)
            self._num_registers = self._get_num_registers(sorted_sequences)
        else:
            self._registers: List[int] = registers
            self._r = self._get_sorted_sequences()
            self._num_registers: int = len(registers)
        

        self._result_path = "results"
        self._save: bool = save_results

    def _get_num_registers(self, sorted_sequences: List[List[int]]) -> int:
        # this function returns the number of registers in the heap result if it is passed instead of the registers list
        num_registers = 0
        for sequence in sorted_sequences:
            num_registers += len(sequence)
        return num_registers

    def _get_sorted_sequences(self) -> None:
        heap = Heap(self._main_memory_size, self._registers)
        sorted_sequences = heap.sort()
        if len(sorted_sequences) != self._num_sorted_sequences:
            raise ValueError(f"The number of sorted sequences is different from the expected {self._num_sorted_sequences}, got {len(sorted_sequences)}")
        
        self._populate_files(sorted_sequences)
    
        """i = 0
        for file in self._files:
            print(f"FILE {i}: ")
            j = 0
            for sequence in file:
                print(f"{j}: {sequence}")
                j += 1
            print()
            i += 1"""
        
    def _populate_files(self, sorted_sequences) -> None:
        for i in range(self._num_sorted_sequences):
            file_index: int = i % self._num_input_files
            self._files[file_index].append(sorted_sequences[i])
            self._index_input_files.add(file_index)

    def _f_print(self, phase: int, beta_value: float, final:bool = False, alpha: Union[None, float] = None) -> None:
        print(f"fase {phase} {beta_value:.2f}")
        for index, file in enumerate(self._files):
            if file:
                print(f"{index + 1}:", end=" ")
                for sequence in file:
                    print("{", end=" ")
                    for register in sequence:
                        print(register, end=" ")
                    print("}", end=" ")
                print()
        if final:
            print(f"final: {alpha:.2f}")

    def sort(self) -> float:
        phase: int = 0
        total_write_operations: int = 0
        while True:
            if phase == 0:
                beta_value:float = beta(self._main_memory_size, self._num_sorted_sequences, self._num_registers, depth=0)
            else:
                num_sequences: int = 0
                sum_size_of_generated_sequences: int = 0
                for index in self._index_input_files:
                    num_sequences += len(self._files[index])
                    for sequence in self._files[index]:
                        # adding the size of all the genererated sequences
                        sum_size_of_generated_sequences += len(sequence)

                total_write_operations += sum_size_of_generated_sequences
                beta_value:float = beta(self._main_memory_size, num_sequences, sum_size_of_generated_sequences, depth=0)
            
            self._f_print(phase, beta_value)
            phase += 1

            if len(self._index_input_files) <= 1 and len(self._files[list(self._index_input_files)[0]]) <= 1:
                break

            # max input index before start the current phase
            max_input_index: int = max(self._index_input_files)

            counter: int = 0

            # accumulator of index input files for the next phase
            accumulator_index_input_files: Set[int] = set()

            while len(self._index_input_files) != 0:
                sequences_to_merge: List[List[int]] = []

                # get the first sequence of each input file
                for index in list(self._index_input_files):
                    file = self._files[index]
                    if file:
                        sequence: List[int] = file.pop(0)
                        sequences_to_merge.append(sequence)

                        if not file:
                            self._index_input_files.remove(index)

                # merge the sequences
                merged_sequence: List[int] = PWays.merge_p_lists(sequences_to_merge)

                # get the index of the output file that will receive the merged sequence
                mod_value: int = self._max_open_files - self._num_input_files
                r_file_index: int = (max_input_index + ((counter % mod_value) + 1)) % self._max_open_files
                counter += 1

                # append the merged sequence to the output file
                self._files[r_file_index].append(merged_sequence)

                # add the index of the output file to the accumulator
                accumulator_index_input_files.add(r_file_index)

            # update the index input files and the number of input files
            self._index_input_files = accumulator_index_input_files
            self._num_input_files = len(self._index_input_files)
            self._num_output_files = self._max_open_files - self._num_input_files
        
        #Wrong?!
        alpha: float = total_write_operations / self._num_registers
        print(f"final: {alpha:.2f}")

        # save the results
        if self._save:
            self._save_results(alpha)

        return alpha
    
    def _save_results(self, alpha: float) -> None:
        if not os.path.exists(self._result_path):
            os.makedirs(self._result_path)

        path: str = os.path.join(self._result_path, f"data_p_ways.txt")
        with open(path, "a") as f:
            f.write(f"{self._r} {alpha}\n")

    @staticmethod
    def merge_p_lists(lists_to_merge: List[List[int]]) -> List[int]:
        if not lists_to_merge:
            return []
        if len(lists_to_merge) == 1:
            return lists_to_merge[0]

        center: int = len(lists_to_merge) // 2
        left: List[int] = PWays.merge_p_lists(lists_to_merge[:center])
        right: List[int] = PWays.merge_p_lists(lists_to_merge[center:])

        return PWays.merge_2_lists(left, right)

    @staticmethod
    def merge_2_lists(left: List[int], right: List[int]) -> List[int]:
        result = []
        i: int = 0
        j: int = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


if __name__ == "__main__":
    registers = [18, 7, 3, 24, 15, 5, 20, 25, 16, 14, 21, 19, 1, 4, 13, 9, 22, 11, 23, 8, 17, 6, 12, 2, 10]
    main_memory_size = 3
    max_open_files = 4
    num_sorted_sequences = 5
    sorted_sequences = [
    [3, 7, 15, 18, 20, 24, 25],
    [5, 14, 16, 19, 21],
    [1, 4, 9, 11, 13, 22, 23],
    [6, 8, 12, 17],
    [2, 10],
    ]

    p_ways = PWays(main_memory_size, num_sorted_sequences, max_open_files, sorted_sequences=sorted_sequences, save_results=False, is_inputing_sorted_sequences=True)
    p_ways.sort()
