#!/usr/bin/env python3
import heapq
from math import inf
from typing import *
import random
import matplotlib.pyplot as plt

#from utils import *

class Polyphasic:
    def __init__(
        self,
        registers: List[int],
        main_memory_size: int,
        num_sorted_sequences: int,
        max_open_files: int,
    ) -> None:
        self.max_open_files = max_open_files
        self.main_memory_size = main_memory_size
        self.num_sorted_size = num_sorted_sequences
        self.registers = registers



    @staticmethod
    def intercalar_sequencias(sequencias):
        resultado = []
        while any(sequencias):
            for seq in sequencias:
                if seq:
                    resultado.append(seq.pop(0))
        return resultado


    def sort(self,seqs):
        m = self.main_memory_size
        r = self.max_open_files
        betas = []
        total_escritas = 0
        total_registros = sum(len(seq) for seq in seqs)

        for j in range(r):
            beta = sum(len(seq) for seq in seqs) / (m * len(seqs))
            betas.append(beta)

            print(f"fase {j} {beta:.2f}")
            for p in range(len(seqs)):
                print(f'{p + 1}: {{', *seqs[p], '}')

            seqs = [sorted(seq) for seq in seqs]
            seqs = [seqs[i] + seqs[i + 1] if i + 1 < len(seqs) else seqs[i] for i in range(0, len(seqs), 2)]

            total_escritas += sum(len(seq) for seq in seqs)

        alpha = total_escritas / total_registros
        print(f"final {alpha:.2f}")
        return seqs, betas, alpha

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

    @staticmethod
    def gerar_sequencias(r, tamanho_max):
        seqs = [random.sample(range(1, 100), tamanho_max) for _ in range(r)]
        return seqs

    @staticmethod
    def realizar_testes(m_vals, r_vals):
        resultados_alpha = []
        resultados_beta = []
        for r in r_vals:
            alphas = []
            betas = []
            for m in m_vals:
                seqs = Polyphasic.gerar_sequencias(r, 10)
                _, beta, alpha = Polyphasic.sort(seqs, r, m)
                alphas.append(alpha)
                betas.append(beta)  # Armazenar todos os valores de beta
            resultados_alpha.append(alphas)
            resultados_beta.append(betas)
        return resultados_alpha, resultados_beta
    @staticmethod
    def plotar_graficos(m_vals, r_vals, resultados_alpha, resultados_beta):
        # Plotando o gráfico de alpha(r) em função de m
        for i, r in enumerate(r_vals):
            plt.plot(m_vals, resultados_alpha[i], label=f'r = {r}')
        plt.xlabel('m (capacidade da memória)')
        plt.ylabel('α(r)')
        plt.title('Gráfico de α(r) em função de m')
        plt.legend()
        plt.show()

        # Plotando o gráfico de beta(m, j) em função de m
        for i, r in enumerate(r_vals):
            for j in range(len(resultados_beta[i][0])):  # Número de fases (j)
                betas_j = [resultados_beta[i][k][j] for k in range(len(m_vals))]
                plt.plot(m_vals, betas_j, label=f'r = {r}, j = {j}')
        plt.xlabel('m (capacidade da memória)')
        plt.ylabel('β(m, j)')
        plt.title('Gráfico de β(m, j) em função de m')
        plt.legend()
        plt.show()



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

    algoritmo = Polyphasic(
        main_memory_size=3,
        registers=[],
        max_open_files=3,
        num_sorted_sequences=1,
    )
    sorted = algoritmo.sort(init_seqs)

    # Parâmetros de Teste
    # m_vals = [2, 3, 4, 5]  # Capacidade da memória
    # r_vals = [2, 3, 4]  # Número de sequências iniciais
    #
    # resultados_alpha, resultados_beta =  Polyphasic.realizar_testes(m_vals, r_vals)
    #
    # # Plotar os Gráficos
    # Polyphasic.plotar_graficos(m_vals, r_vals, resultados_alpha, resultados_beta)

    # sorted = Polyphasic(
    #     registers = init_seqs,
    #     initial_seq_size = 1,
    #     num_sorted_sequences = 49,
    #     max_open_files = 5,
    # )
    #print(seq_to_notation(sorted))
