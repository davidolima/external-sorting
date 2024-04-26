from typing import List, Set
from heap import Heap
import math


class PWays:

    def __init__(self, main_memory_size: int, registers: List[int],
                 num_sorted_sequences: int, max_open_files: int) -> None:

        self._main_memory_size: int = main_memory_size
        self._registers: List[int] = registers
        self._num_sorted_sequences: int = num_sorted_sequences
        self._max_open_files: int = max_open_files
        self._files: List[List[List[int]]] = [[] for _ in range(max_open_files)]

        self._num_input_files: int = math.floor(max_open_files / 2)
        self._index_input_files: Set[int] = set()

        self._num_output_files: int = math.ceil(max_open_files / 2)
        self._index_output_files: Set[int] = set()

        self._get_sorted_sequences()

    def _get_sorted_sequences(self) -> None:
        heap = Heap(self._main_memory_size, self._registers, self._num_sorted_sequences)
        sorted_sequences = heap.sort()
        """print(sorted_sequences)
        print()"""

        for i in range(self._num_sorted_sequences):
            file_index: int = i % self._num_input_files
            self._files[file_index].append(sorted_sequences[i])
            self._index_input_files.add(file_index)

        """i = 0
        for file in self._files:
            print(f"FILE {i}: ")
            j = 0
            for sequence in file:
                print(f"{j}: {sequence}")
                j += 1
            print()
            i += 1"""

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
    """registers = [18, 7, 3, 24, 15, 5, 20, 25, 16, 14, 21, 19, 1, 4, 13, 9, 22, 11, 23, 8, 17, 6, 12, 2, 10]
    main_memory_size = 2
    max_open_files = 4
    num_sorted_sequences = 7
    p_caminhos = PCaminhos(main_memory_size, registers, num_sorted_sequences, max_open_files)
    p_caminhos.get_sorted_sequences()"""
    lists = [[1, 12, 3], [4, 5, 18], [7, 8, 9]]
    resultado = PWays.merge_p_lists(lists_to_merge=lists)
    print(resultado)
