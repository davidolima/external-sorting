#!/usr/bin/env python3

from logging import debug
from matplotlib.font_manager import generate_fontconfig_pattern
from utils.heap import Heap
from utils.utils import togglePrint, beta

from methods.p_ways import PWays
from methods.cascade import Cascade
from methods.polyphasic import Polyphasic

import os
import random
import time, datetime
from typing import *

from tqdm import tqdm

import matplotlib.pyplot as plt

class Evaluator():
    def __init__(self, algoritmo: Literal["B", "P", "C"], output_path: Optional[str] = None) -> None:
        self.algoritmo = algoritmo.upper()
        assert self.algoritmo in ("B","P","C"), f"Algoritmo não reconhecido: `{self.algoritmo}`"
        print(f"Running with {self.get_alg_name()} sort.")

        self.output_path = output_path
        assert os.path.isdir(self.output_path), "Please select a directory as an output path."

    @staticmethod
    def _generate_random_sequence(size: Optional[int | Tuple[int,int]] = None, low=0, high=100) -> List[int]:
        if size is None:
            size = random.randint(4,10)
        elif type(size) == tuple:
            size = random.randint(size[0], size[1])

        assert type(size) == int, "Unreachable."
        return [random.randint(low, high) for _ in range(size)]

    @staticmethod
    def _generate_ordered_runs(size = None, low=0, high=100, main_memory_size=3, max_seq_len=5):
        runs = Evaluator._generate_random_runs(size, low,  high, main_memory_size, max_seq_len)
        [x.sort() for x in runs]
        return runs

    @staticmethod
    def _generate_random_runs(size = None, low=0, high=100, main_memory_size=3, max_seq_len=5) -> List[List[int]]:
        size = size if size is not None else random.randint(4, 10)
        return [Evaluator._generate_random_sequence(random.randint(main_memory_size, max_seq_len), low, high) for _ in range(size)]

    def get_alg_name(self):
        match (self.algoritmo):
            case 'B': return "PWays"
            case 'P': return "Polyphasic"
            case 'C': return "Cascade"
            case _: raise Exception("Unreachable.")

    def generate_graph(self, x, y, x_label, y_label, title = None, fpath = None, legend = None) -> None:
        assert self.output_path is not None, "You need to set `self.output_path` to generate a graph."

        if fpath is None:
            curr_time_str = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            fpath = os.path.join(self.output_path, f"{self.get_alg_name()}_graph-{curr_time_str}.png")

        title = f"{x_label} x {y_label}" if title is None else title
        print("[!] Generating graph...", end=' ')

        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        if legend is not None:
            plt.legend(legend)
        plt.savefig(fpath)
        print(f"Done. Saved to `{fpath}`.")
    
    def run_with_r_sequences(self, r: int, m: int, k: int) -> float:
        togglePrint() # Disable printing

        if self.algoritmo == "B":
            initial_sequences = self._generate_random_runs(r, main_memory_size=m)

            alg = PWays(
                main_memory_size=m,
                num_sorted_sequences=len(initial_sequences),
                max_open_files=k,
                sorted_sequences=initial_sequences,
                save_results=False,
                is_inputing_sorted_sequences=True
            )

            #for i in range(len(initial_sequences)):
                #file_index: int = i % alg._num_input_files
                #sorted_sequence = sorted(initial_sequences[i])
                #alg._files[file_index].append(sorted_sequence)
                #alg._index_input_files.add(file_index)

        elif self.algoritmo == 'P':
            initial_sequences = Evaluator._generate_ordered_runs(size=r, main_memory_size=m)

            alg = Polyphasic(
                registers=[],
                main_memory_size=m,
                num_sorted_sequences=r,
                max_open_files=k,
            )

            _, alpha, _ = alg.sort(data=initial_sequences, verbose=False)
            togglePrint() # Re-enable printing

            return alpha

        else: # Cascade
            seqs = Evaluator._generate_ordered_runs(size=r)
            alg = Cascade(
                registers=seqs,
                main_memory_size=m,
                max_open_files=k,
                verbose=True,
            )

        try:
            alpha = alg.sort()
            togglePrint() # Re-enable printing
        except Exception as e:
            # In case of error, rerun the algorithm with
            # printing enabled while using same cfg
            # to understand what happened.
            togglePrint() # Re-enable printing
            alg.sort()

        return alpha

    def test_alpha(self, m: int, k: int, r_values: List[int], save_results: bool = False) -> List[float]:
        results = []

        start_time = time.perf_counter()
        for i in tqdm(r_values):
            result = self.run_with_r_sequences(r=i, m=m, k=k)
            results.append(result)
        end_time = time.perf_counter()

        print(f"[!] Ran {len(r_values)} tests in {end_time - start_time} seconds.")

        if save_results:
            assert self.output_path is not None, "You need to define an output dir to be able to save the results."
            if os.path.isdir(self.output_path):
                fpath = os.path.join(self.output_path, f"alpha_test_{self.get_alg_name()}_m{m}_k{k}.csv")
            else:
                fpath = self.output_path

            print("[!] Saving results...", end=' ')
            with open(fpath, 'w+') as f:
                for i in r_values:
                    f.write(f"{i}, {results[i]:.2f}\n")

            print(f"Done. Results saved to `{fpath}`.")

        return results

    def test_k(
        self,
        m: int,
        k_values: List[int],
        r_values: List[int],
        save_results: bool = False,
        generate_graph: bool = True
    ) -> List[float]:
        start_time = time.perf_counter()
        for i in tqdm(k_values):
            alphas = self.test_alpha(m=m, k=i, r_values=r_values, save_results = False)

            if save_results:
                assert self.output_path is not None, "You need to define an output dir to be able to save the results."
                print("[!] Saving results...", end=' ')
                fpath  = os.path.join(self.output_path, f"m_test_{self.get_alg_name()}_m{m}_k{i}")

                with open(fpath + ".csv", 'w+') as f:
                    for i in range(len(alphas)):
                        f.write(f"{i}, {alphas[i]:.2f}\n")

                print(f"Results of k={i} saved to `{fpath}.csv`.", end=' ')
                print()

            if generate_graph:
                assert self.output_path is not None, "You need to define an output dir to be able to save the results."
                fpath  = os.path.join(self.output_path, f"m_test_{self.get_alg_name()}_m{m}_k{i}")
                plt.style.use('ggplot')
                evaluator.generate_graph(
                    x = r_values,
                    y = alphas,
                    x_label = r"Nº Sequencias iniciais ($r$)",
                    y_label = r"Taxa de processamento ($\alpha$)",
                    title=self.get_alg_name(),
                    fpath=fpath + '.png',
                    legend=[f"k={x}" for x in k_values],
                )


        end_time = time.perf_counter()
        print(f"[!] Ran {len(k_values)} tests in {end_time - start_time} seconds.")

        return alphas

    def test_k_for_all(
        self,
        m: int,
        k_values: List[int],
        r_values: List[int],
        algorithms: Tuple[Literal["B"], Literal["P"], Literal["C"]] = ("B", "P", "C"),
        save_results: bool = True,
        generate_graph: bool = True,
    ):
        for alg in algorithms:
            plt.clf()
            self.algoritmo = alg
            self.test_k(
                m=m,
                k_values=k_values,
                r_values=r_values,
                save_results=save_results,
                generate_graph=generate_graph
            )

    def test_beta(
            self,
            m_values: List[int],
            N_OF_REGS: int = 500,
            save_results: bool = False,
            generate_graph: bool = False,
            fixed_seq: bool = False,
    ) -> None:
        betas = []
        heap_results = []
        if fixed_seq:
            regs = Evaluator._generate_random_sequence(N_OF_REGS)

        print("Fixed sequence:", regs)
        for m in tqdm(m_values):
            if not fixed_seq:
                regs = Evaluator._generate_random_sequence(N_OF_REGS)
            sorted_seqs = Heap(
                main_memory_size=m,
                registers=regs
            ).sort()

            heap_results.append(sorted_seqs)
            betas.append(
                beta(m, len(sorted_seqs), N_OF_REGS, depth=0)
            )

        if save_results:
            assert self.output_path is not None, "You need to define an output dir to be able to save the results."
            print("[!] Saving results...", end=' ')
            fpath  = os.path.join(self.output_path, f"beta_test_m{m}" if not fixed_seq else f"beta_test_m{m}_fixed")

            with open(fpath + ".csv", 'w+') as f:
                for i in range(len(betas)):
                    f.write(f"{i}, {betas[i]:.2f} , {heap_results[i]}\n")

            print(f"Results of k={i} saved to `{fpath}.csv`.", end=' ')
        print()

        if generate_graph:
            assert self.output_path is not None, "You need to define an output dir to be able to save the results."
            fpath  = os.path.join(self.output_path, f"beta_test_m{m}" if not fixed_seq else f"beta_test_m{m}_fixed")
            plt.style.use('ggplot')
            evaluator.generate_graph(
                x = m_values,
                y = betas,
                x_label = r"Tam. da memória principal ($m$)",
                y_label = r"$\beta$",
                fpath=fpath + '.png',
                legend=[f"m={x}" for x in m_values],
            )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algorithms",        type=str, default='C')
    parser.add_argument("-m", "--main-memory-size",  type=int, default=3)
    parser.add_argument("-o", "--output",            type=str, default="results/")
    args = parser.parse_args()

    evaluator = Evaluator(
        algoritmo=args.algorithms,
        output_path=args.output
    )

    # r_values = []
    # for i in range(1,11): # R = {i x j <= 5000 | i = 1, 2, ... , 10; j = 10, 20, ... , 1000}
    #     for j in range(10,1001,10):
    #         if i*j <= 5000 and not i*j in r_values:
    #             r_values.append(i*j)
    # r_values = sorted(r_values)

    # evaluator.test_k_for_all(
    #     algorithms=("B", "P", "C"),
    #     m=args.main_memory_size,
    #     k_values=list(range(4,13,2)),
    #     r_values=r_values,
    #     save_results=True,
    #     generate_graph=True
    # )

    m_values = [1] + [3*(5*i) for i in range(1,5)]
    evaluator.test_beta(
        m_values=list(range(3,61)),#m_values,
        save_results=True,
        generate_graph=True,
        N_OF_REGS=500,
        fixed_seq=True,
    )
