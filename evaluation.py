#!/usr/bin/env python3

from utils.heap import Heap
from utils.utils import togglePrint

from methods.p_ways import PWays
from methods.cascade import Cascade
from methods.polyphasic import Polyphasic

import os
import random
import time, datetime

import matplotlib.pyplot as plt

class Evaluator():
    def __init__(self, algoritmo, output_path: str = None):
        self.algoritmo = algoritmo
        assert self.algoritmo in ("B","P","C"), f"Algoritmo não reconhecido: `{self.algoritmo}`"
        print(f"Running with {self.get_alg_name()} sort.")

        self.output_path = output_path
        assert os.path.isdir(self.output_path), "Please select a directory as an output path."

    def _generate_random_sequence(self, size = None, low=0, high=100):
        size = size if size is not None else random.randint(4, 10)
        return [random.randint(low, high) for _ in range(size)]

    def _generate_random_runs(self, size = None, low=0, high=100, main_memory_size=3, max_seq_len=5):
        size = size if size is not None else random.randint(4, 10)
        return [[self._generate_random_sequence(random.randint(main_memory_size, max_seq_len), low, high)] for _ in range(size)]

    def get_alg_name(self):
        match (self.algoritmo):
            case 'B': return "PWays"
            case 'P': return "Polyphasic"
            case 'C': return "Cascade"
            case _: raise Exception("Unreachable.")

    def generate_graph(self, x, y, x_label, y_label, title = None):
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
    
    def run_with_r_sequences(self, r: int, m: int, k: int):
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
                alg._registers.extend(x[0])

            for i in range(len(initial_sequences)):
                file_index: int = i % alg._num_input_files
                sorted_sequence = sorted(initial_sequences[i])
                alg._files[file_index].append(sorted_sequence)
                alg._index_input_files.add(file_index)

        elif self.algoritmo == 'P':
            initial_sequences = self._generate_random_runs(size=r, main_memory_size=m)
            alg = Polyphasic(
                registers=[],
                main_memory_size=m,
                num_sorted_sequences=r,
                max_open_files=k,
            )
            alg.registers = []
            for x in initial_sequences:
                alg.registers.extend(x[0])

            togglePrint()
            _, alpha, _ = alg.sort(initial_sequences)
            togglePrint()

            return alpha

        else:
            regs = self._generate_random_sequence(size=r)
            alg = Cascade(
                registers=regs,
                max_open_files=k,
                verbose=False,
            )

        togglePrint() # Disable printing
        alpha = alg.sort()
        togglePrint() # Re-enable it

        return alpha

    def test_alpha(self, m: int, k: int, r_lower_limit: int, r_upper_limit: int, save_results: bool = False):
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
