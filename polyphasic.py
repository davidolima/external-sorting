#!/usr/bin/env python3

from math import inf
from typing import *

#from utils import *

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
    def intercalar_sequencias(sequencias):
        resultado = []
        while any(sequencias):
            for seq in sequencias:
                if seq:
                    resultado.append(seq.pop(0))
        return resultado

    @staticmethod
    def intercalacao_polifasica(seqs, r, m):
        betas = []
        for j in range(r):
            beta = sum(len(seq) for seq in seqs) / (m * len(seqs))
            betas.append(beta)

            print(f"fase {j} {beta:.2f}")
            for p in range(len(seqs)):
                print(f'{p + 1}:',*seqs[p])

            seqs = [sorted(seq) for seq in seqs]
            seqs = [seqs[i] + seqs[i + 1] if i + 1 < len(seqs) else seqs[i] for i in range(0, len(seqs), 2)]

        alpha = sum(len(seq) for seq in seqs) / sum(len(s) for s in seqs)
        print(f"final {alpha:.2f}")
        return seqs

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

    # init_seqs = [
    #         [random.randint(1, 100) for i in range(12)],
    #         [random.randint(1, 100) for i in range(8)],
    #         [random.randint(1, 100) for i in range(14)],
    #         [random.randint(1, 100) for i in range(15)],
    #         [],
    # ]

    init_seqs = [
        [1,5,6,7,8],
        [1,3,4,7],
        [2,3,4,9,10],
        []
    ]

    [x.sort() for x in init_seqs]
    print(f"Sequências iniciais ({len(init_seqs)}):")
    [print(seq) for seq in init_seqs]
    print("Organização inicial:")
    #print(seq_to_notation(init_seqs))


    r=3
    m=3
    sorted = Polyphasic.intercalacao_polifasica(init_seqs, r, m)
    print(f"Sorted:", *sorted[0])
    # sorted = Polyphasic(
    #     registers = init_seqs,
    #     initial_seq_size = 1,
    #     num_sorted_sequences = 49,
    #     max_open_files = 5,
    # )
    #print(seq_to_notation(sorted))
