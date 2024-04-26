from typing import List, Union


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
            raise ValueError("The node is already marked")

    def unmark(self) -> None:
        if self._is_marked:
            self._is_marked = False
        else:
            raise ValueError("The node is already unmarked")

    def __gt__(self, other: 'Node') -> bool:
        if self._is_marked and not other._is_marked:
            return True
        elif not self._is_marked and other._is_marked:
            return False
        else:
            return self._value > other._value

    def __ge__(self, other: 'Node') -> bool:
        if self._is_marked and not other._is_marked:
            return True
        elif not self._is_marked and other._is_marked:
            return False
        else:
            return self._value >= other._value


class Heap:
    def __init__(self, main_memory_size: int, registers: List[int], num_sorted_sequences: int) -> None:
        self._main_memory_size: int = main_memory_size
        self._registers: List[int] = registers
        self._num_sorted_sequences: int = num_sorted_sequences
        self._last_min_node: Union[None, Node] = None
        self._heap_size: int = 0
        self._sorted_sequences: List[List[int]] = [[] for _ in range(num_sorted_sequences)]
        self._i_sorted_sequence: int = 0
        self._heap: List[Node] = []
        self._fill_heap()

    @staticmethod
    def _parent(i: int) -> int:
        return (i - 1) // 2

    @staticmethod
    def _left(i: int) -> int:
        return 2 * i + 1

    @staticmethod
    def _right(i: int) -> int:
        return 2 * i + 2

    def _swap(self, i: int, j: int) -> None:
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

    def _min_heapify(self, i: int) -> None:
        left = self._left(i)
        right = self._right(i)
        smallest = i
        if left < self._heap_size and self._heap[left] < self._heap[i]:
            smallest = left
        if right < self._heap_size and self._heap[right] < self._heap[smallest]:
            smallest = right
        if smallest != i:
            self._swap(i, smallest)
            self._min_heapify(smallest)

    def _build_min_heap(self) -> None:
        for i in range(self._heap_size // 2, -1, -1):
            self._min_heapify(i)

    def _extract_min(self) -> Node:
        if self._heap_size < 1:
            raise ValueError("Heap underflow")
        min_node = self._heap[0]
        self._last_min_node = min_node

        self._heap[0] = self._heap[self._heap_size - 1]
        self._heap.remove(self._heap[self._heap_size - 1])

        self._heap_size -= 1
        self._min_heapify(0)
        return min_node

    def _insert(self, node: Node) -> None:
        self._heap_size += 1
        if self._heap_size > self._main_memory_size:
            raise ValueError("Heap overflow")

        if self._last_min_node is not None and node < self._last_min_node:
            node.mark()

        self._registers.pop(0)

        self._heap.append(node)
        i = self._heap_size - 1
        while i > 0 and self._heap[self._parent(i)] > self._heap[i]:
            self._swap(i, self._parent(i))
            i = self._parent(i)

    def _fill_heap(self) -> None:
        if self._main_memory_size <= len(self._registers):
            for i in range(self._main_memory_size):
                self._insert(Node(self._registers[0]))
        else:
            for i in range(len(self._registers)):
                self._insert(Node(self._registers[0]))

    def _check_marked_nodes(self) -> None:
        if all([node.is_marked for node in self._heap]):
            self._unmark_nodes()
            self._i_sorted_sequence += 1
            if self._i_sorted_sequence >= self._num_sorted_sequences:
                raise ValueError("Sorted sequences overflow")

    def _unmark_nodes(self) -> None:
        for node in self._heap:
            node.unmark()

    def sort(self) -> List[List[int]]:
        while self._heap_size > 0:
            self._check_marked_nodes()
            min_node = self._extract_min()
            self._sorted_sequences[self._i_sorted_sequence].append(min_node.value)
            if len(self._registers) > 0:
                self._insert(Node(self._registers[0]))
        return self._sorted_sequences


if __name__ == "__main__":
    registers: List[int] = [18, 7, 3, 24, 15, 5, 20, 25, 16, 14, 21, 19, 1, 4, 13, 9, 22, 11, 23, 8, 17, 6, 12, 2, 10]
    main_memory_size: int = 3
    num_sorted_sequences: int = 5
    heap = Heap(main_memory_size, registers, num_sorted_sequences)
    sorted_sequences = heap.sort()
    print(sorted_sequences)
