#!/usr/bin/env python3

from logging import debug
from matplotlib.font_manager import generate_fontconfig_pattern
from utils.heap import Heap
from utils.utils import togglePrint

from methods.p_ways import PWays
from methods.cascade import Cascade
from methods.polyphasic import Polyphasic

import os
import random
import time, datetime
from typing import *

import matplotlib.pyplot as plt

class Evaluator():
    def __init__(self, algoritmo, output_path: Optional[str] = None) -> None:
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

    def generate_graph(self, x, y, x_label, y_label, title = None) -> None:
        assert self.output_path is not None, "You need to set `self.output_path` to generate a graph."

        curr_time_str = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        fpath = os.path.join(self.output_path, f"{self.get_alg_name()}_graph-{curr_time_str}.png")
        title = f"{x_label} x {y_label}" if title is None else title
        print("[!] Generating graph...", end=' ')
        plt.plot(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.savefig(fpath)
        print(f"Done. Saved to `{fpath}`.")
    
    def run_with_r_sequences(self, r: int, m: int, k: int) -> float:
        togglePrint() # Disable printing

        if self.algoritmo == "B":
            initial_sequences = self._generate_random_runs(r, main_memory_size=m)

            alg = PWays(
                main_memory_size=m,
                registers=[],
                max_open_files=k,
                num_sorted_sequences=1,

            )
            alg._registers = []
            alg._files = [[] for _ in range(k)]
            alg._r = len(initial_sequences)
            alg._num_sorted_sequences=len(initial_sequences)

            for x in initial_sequences:
                alg._registers.extend(x)

            for i in range(len(initial_sequences)):
                file_index: int = i % alg._num_input_files
                sorted_sequence = sorted(initial_sequences[i])
                alg._files[file_index].append(sorted_sequence)
                alg._index_input_files.add(file_index)

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

        else:
            seqs = Evaluator._generate_random_runs(size=r)
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

    def test_alpha(self, m: int, k: int, r_lower_limit: int, r_upper_limit: int, save_results: bool = False) -> List[float]:
        results = []

        start_time = time.perf_counter()
        for i in range(r_lower_limit, r_upper_limit):
            result = self.run_with_r_sequences(r=i, m=m, k=k)
            results.append(result)
        end_time = time.perf_counter()

        print(f"[!] Ran {r_upper_limit - r_lower_limit} tests in {end_time - start_time} seconds.")

        if save_results:
            assert self.output_path is not None, "You need to define an output dir to be able to save the results."
            if os.path.isdir(self.output_path):
                fpath = os.path.join(self.output_path, f"alpha_test_{self.get_alg_name()}.csv")
            else:
                fpath = self.output_path

            print("[!] Saving results...", end=' ')
            with open(fpath, 'w+') as f:
                for i in range(len(results)):
                    f.write(f"{i + r_lower_limit}, {results[i]:.2f}\n")

            print(f"Done. Results saved to `{fpath}`.")

        return results



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--algoritmo",        type=str, default='C')
    parser.add_argument("-m", "--main-memory-size", type=int, default=3)
    parser.add_argument("-k", "--max-open-files",   type=int, default=4)
    parser.add_argument("-rl", "--r-lower-limit",   type=int, default=3)
    parser.add_argument("-ru", "--r-upper-limit",   type=int, default=100)
    parser.add_argument("-o", "--output",           type=str, default="results/")
    args = parser.parse_args()

    evaluator = Evaluator(
        algoritmo=args.algoritmo,
        output_path=args.output
    )

    alphas = evaluator.test_alpha(
        m=args.main_memory_size,
        k=args.max_open_files,
        r_lower_limit=args.r_lower_limit,
        r_upper_limit=args.r_upper_limit,
        save_results=True
    )

    plt.style.use('ggplot')
    evaluator.generate_graph(
        x = list(range(int(args.r_lower_limit),int(args.r_upper_limit))),
        y = alphas,
        x_label = r"Nº Sequencias iniciais ($r$)",
        y_label = r"Taxa de processamento ($\alpha$)",
        title=f"m={args.main_memory_size} k={args.max_open_files}"
    )
