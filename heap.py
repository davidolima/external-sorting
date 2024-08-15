from typing import List
class Node:
    
    def __init__(self, value: int) -> None:
        self._value: int = value
        self._is_marked: bool = False

    @property
    def value(self) -> int:
        return self._value
    
    @property
    def is_marked(self) -> bool:
        return self._is_marked
    
    def mark(self) -> None:
        if not self._is_marked:
            self._is_marked = True
        else:
            raise ValueError("the node is already marked")

    def unmark(self) -> None:
        if self._is_marked:
            self._is_marked = False
        else:
            raise ValueError("the node is already unmarked")
        
    def __gt__(self, other) -> bool:
        if self._is_marked and not other._is_marked:
            return True
        elif not self._is_marked and other._is_marked:
            return False
        else:
            return self._value > other._value
    
    def __ge__(self, other) -> bool:
        if self._is_marked and not other._is_marked:
            return True
        elif not self._is_marked and other._is_marked:
            return False
        else:
            return self._value >= other._value

class Heap:

    def __init__(self, main_memory_size: int, registers: List[int], num_sorted_sequences: int):
        self._main_memory_size: int = main_memory_size
        self._registers: List[int] = registers
        self._num_sorted_sequences: int = num_sorted_sequences

        self._heap_size: int = 0

        self._sorted_sequences: List[List[int]] = [[] for _ in range(num_sorted_sequences)]
        self._i_sorted_sequence: int = 0

        self._heap: List[Node] = []

    def _parent(self, i: int) -> int:
        return (i - 1) // 2
    
    def _left(self, i: int) -> int:
        return 2 * i + 1
    
    def _right(self, i: int) -> int:
        return 2 * i + 2
    
    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _min_heapify(self, i: int) -> None:
        l = self._left(i)
        r = self._right(i)
        smallest = i
        if l < self._heap_size and self._heap[l] < self._heap[i]:
            smallest = l
        if r < self._heap_size and self._heap[r] < self._heap[smallest]:
            smallest = r
        if smallest != i:
            self._swap(i, smallest)
            self._min_heapify(smallest)

    def _build_min_heap(self) -> None:
        for i in range(self._heap_size // 2, -1, -1):
            self._min_heapify(i)
    
    def _extract_min(self) -> Node:
        if self._heap_size < 1:
            raise ValueError("heap underflow")
        min_node = self._heap[0]
        self._heap[0] = self._heap[self._heap_size - 1]
        self._heap_size -= 1
        self._min_heapify(0)
        return min_node

    def _insert(self, node: Node) -> None:
        self._heap_size += 1
        if self._heap_size > self._main_memory_size:
            raise ValueError("heap overflow")
        
        if self._heap_size > 1 and self._heap[0] < node:
            node.mark()

        self._registers.pop(0)
        self._heap.append(node)
        i:int = self._heap_size - 1
        while i > 0 and self._heap[self._parent(i)] > self._heap[i]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _unmark_nodes(self) -> None:
        for node in self._heap:
            node.unmark()

   

if __name__ == "__main__":
    registers = [18, 7, 3, 24, 15, 5, 20, 25, 16, 14, 21, 19, 1, 4, 13, 9, 22, 11, 23, 8, 17, 6, 12, 2, 10]
    main_memory_size = 3
    num_sorted_sequences = 5
    heap = Heap(main_memory_size, registers, num_sorted_sequences)
    