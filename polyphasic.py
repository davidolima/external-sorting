#!/usr/bin/env python3

from math import inf
from typing import *

from utils import *

class Polyphasic:
    def __init__(
        self,
        registers: List[int],
        initial_seq_size: int,
        num_sorted_sequences: int,
        max_open_files: int,
    ) -> None:
        self.max_open_files = max_open_files
        self.initial_seq_size = initial_seq_size
        self.num_sorted_size = num_sorted_sequences
        self.registers = registers

    def _generate_initial_sequences(self) -> List[List[List[int]]]:
        # TODO: Mudar para Heap.
        return [
            [[random.randint(1, 100)] for i in range(12)],
            [[random.randint(1, 100)] for i in range(8)],
            [],
            [[random.randint(1, 100)] for i in range(14)],
            [[random.randint(1, 100)] for i in range(15)],
        ]

    @staticmethod
    def merge_n_lists(LL: List[List[int]]) -> List[int]:
        """
        Args:
         LL: List of sequences of registers.
        """
        m: int = len(LL)
        out: List[int] = []
        iters = [0] * m

        while True:
            # Pegar elementos de cada lista, apontados por cada índice em `iters`.
            current_elements: List[int] = [LL[i][iters[i]] for i in range(len(LL))] # Lista com todos os elementos sendo avaliados
            current_elements = [current_elements[i] if iters[i] >= 0 else inf for i in range(len(LL))] # Substituir elementos com índice < 0 por `inf`
            smallest_elem_idx: int = argmin(current_elements)
            smallest_elem = current_elements[smallest_elem_idx]
            if smallest_elem == inf: break

            out.append(current_elements[smallest_elem_idx])
            # Incrementar índice da lista correspondente
            iters[smallest_elem_idx] += 1
            if iters[smallest_elem_idx] >= len(LL[smallest_elem_idx]):
                iters[smallest_elem_idx] = -1

        return out

    @staticmethod
    def indice_lista_vazia(lista):
        for i, sublist in enumerate(lista):
            if len(sublist) == 0:
                return i
        return -1

    @staticmethod
    def intercalacao_polifasica(seqs):
        result = []
        output_tape = []
        fase = 0

        print(f"Fase {fase}. Estado das fitas:")
        for i, tape in enumerate(seqs):
            print(f"Fita {i + 1}: {tape}")
        fase += 1

        while len(seqs) > 1:
            current = []
            for c in range(len(seqs)):
                if len(seqs[c]) > 0:
                    current.append((seqs[c][0], c))
            if not current:
                break

            number, index = min(current)
            result.append(number)
            seqs[index].pop(0)

            empty_list_index = Polyphasic.indice_lista_vazia(seqs)
            if empty_list_index != -1:
                output_tape = seqs.pop(empty_list_index)
                print(f"Fase {fase}. Estado das fitas:")
                fase += 1
                for i, tape in enumerate(seqs):
                    print(f"Fita {i + 1}: {tape}")

        result.extend(output_tape)
        return result

    @staticmethod
    def merge_2_lists(A: List[int], B: List[int], C: List[int]) -> List[int]:
        """
        A, B: Listas que serão mescladas.
        C: Lista vazia de saída.
        """
        iter_a = iter(A)
        iter_b = iter(B)
        a = next(iter_a, -1)
        b = next(iter_b, -1)
        while (a != -1 and b != -1):
            if a > b:
                B.remove(b)
                C.append(b)
                b = next(iter_b, -1)
            else:
                A.remove(a)
                C.append(a)
                a = next(iter_a, -1)

        # Se não houver mais elementos em A, adiciona os elementos restantes
        # de B em C.
        if (a == -1):
            while (b != -1):
                C.append(b)
                b = next(iter_b, -1)
            return C

        # Caso simétrico ao anterior, porém para B vazio.
        while (a != -1):
            C.append(a)
            a = next(iter_a, -1)
        return C

if __name__ == "__main__":
    import random
    #Por enquanto, o algoritmo apaga as listas vazias a fim de evitar um loop infinito
    #Estou resolvendo isso, mas ele já retorna os valores ordenados
    #Além disso também estou com problema pra identificar o fim da fase nesse algoritmo
    #TODO: resolver os problemas citados acima

    init_seqs = [
            [random.randint(1, 100) for i in range(12)],
            [random.randint(1, 100) for i in range(8)],
            [random.randint(1, 100) for i in range(14)],
            [random.randint(1, 100) for i in range(15)],
            [],
    ]

    [x.sort() for x in init_seqs]
    print(f"Sequências iniciais ({len(init_seqs)}):")
    [print(seq) for seq in init_seqs]
    print("Organização inicial:")
    #print(seq_to_notation(init_seqs))


    sorted = Polyphasic.intercalacao_polifasica(init_seqs)
    print(f"Sorted: {sorted}")
    # sorted = Polyphasic(
    #     registers = init_seqs,
    #     initial_seq_size = 1,
    #     num_sorted_sequences = 49,
    #     max_open_files = 5,
    # )
    #print(seq_to_notation(sorted))
