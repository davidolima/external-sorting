#!/usr/bin/env python3

import sys
sys.path.append('..')

from typing import *
#from polyphasic import Polyphasic
from utils.heap import Heap
from utils.utils import beta

class Cascade:
    def __init__(
        self,
        registers: List[int],
        max_open_files: int,

        verbose: bool = True,
        _debug: bool = False,
    ) -> None:

        self.registers = registers
        self.max_open_files = max_open_files

        self._files = [[] for _ in range(max_open_files)]
        self.write_ops_per_phase = []
        self._fase = 0

        self.verbose = verbose
        self._debug = _debug

        self._distribute_registers_in_files()

    @staticmethod
    def _calculate_ideal_previous_line(line: List[int]) -> List[int]:
        r = [0]*len(line)
        curr_line = line.copy()
        # Weird way of doing it, but it moves the empty file around
        valid_idxs = list(range(len(line)))
        valid_idxs.remove(line.index(max(line)))
        for i in valid_idxs:
            curr_line.remove(min(curr_line))
            r[i] = sum(curr_line)
        return r
    
    @staticmethod
    def _alternate_ideal_previous_line(line: List[int]) -> List[int]:
        if line.count(0) > 1:
            # [_, _, 1, _] => [1, 1, _, 1]
            return [1 if x == 0 else 0 for x in line]
            
        idx_max = line.index(max(line))

        if idx_max == len(line)-1:
            next_line = [sum(line[p:]) for p in range(1, len(line))]
            return next_line + [0]
        
        next_line = [sum(line[:p]) for p in range(1, len(line))]
        return [0] + next_line

    @staticmethod
    def _get_ideal_initial_seq_sizes(n_seqs: int, max_open_files: int, _debug=False) -> List[int]:
        curr_line = [0] * max_open_files
        curr_line[-1] = 1
        if _debug: print(curr_line)
        while (sum(curr_line) < n_seqs):
            curr_line = Cascade._calculate_ideal_previous_line(curr_line)
            if _debug: print(curr_line)
        return curr_line

    def _distribute_registers_in_files(self) -> None:
        tam_inicial_ideal = Cascade._get_ideal_initial_seq_sizes(
            len(self.registers),
            self.max_open_files,
            _debug = self._debug,
        )
        tam_inicial_ideal.remove(0)

        registers = self.registers.copy()
        write_ops = 0
        file_idx = 0
        while len(registers) > 0:
            if len(self._files[file_idx%(len(self._files)-1)]) == tam_inicial_ideal[file_idx%(len(self._files)-1)]:
                file_idx += 1
                continue

            self._files[file_idx%(len(self._files)-1)].append([registers.pop()])

            write_ops += 1
            file_idx += 1

        for i in range(self.max_open_files-1):
            # Complete the ideal size with dummy runs.
            n_dummy_runs = tam_inicial_ideal[i] - len(self._files[i])
            self._files[i].extend([[float('inf')] for _ in range(n_dummy_runs)])

        # Do we need to count the number of write ops when first distributing
        # the sequences on files?
        self.write_ops_per_phase.append(0)#(write_ops)
        self._print_fase()

    def _print_fase(self):
        """
        Imprime o estado da fase atual na notação pedida.
        """
        if not self.verbose:
            return
        
        stringify = lambda s: str(s)[1:-1].replace('[','{').replace(']','}').replace(',', '')

        print(f"fase {self._fase} {self._calculate_current_beta():.2f}")
        total = 0
        for i, s in enumerate(self._files):
            if len(s) == 0:
                continue
            line_str  = str(i+1)
            if self._debug:
                # Qtd. + tam. das seqs.
                line_str += '(' + str(len(s)) + (')' if len(s) < 1 else (',' + str(len(s[0])) + ')'))
                total += sum([len(x) for x in s])
            line_str += ": " + stringify(s)
            print(line_str)
        if self._debug: print("n_total_seqs:", total)

        self._fase+=1

    def _calculate_alpha(self):
        alpha = (sum(self.write_ops_per_phase) / len(self.registers)) if len(self.registers) != 0 else 0
        return alpha

    def get_beta_at_phase(self, phase: int = -1):
        """
        NOTE: If `phase` is not specified, considers the last phase calculated.
        """

        assert -1 <= phase < len(self.write_ops_per_phase), f"There is no phase `{phase}`"

        if phase < 0:
            num_sequences = sum([len(x) for x in self._files])
        else:
            num_sequences = sum([len(x) for x in self._files[:phase+1]])
        write_ops_at_phase = self.write_ops_per_phase[phase]  # Last entry on the list

        if self._debug: print("num_sequences:", num_sequences, "write_ops_at_phase:", write_ops_at_phase)

        return beta(
            self.main_memory_size,
            num_sequences,
            write_ops_at_phase,
        )

    def _calculate_current_beta(self):
        return self.get_beta_at_phase(-1)

    def merge_files(self, file_idxs: list[int]) -> list[int]:
        sequences = [self._files[i].pop(0) for i in file_idxs]
        
        out = []

        while not any([len(x) == 0 for x in sequences]):
            current_elements: list[int] = [sequences[i][0] for i in range(len(sequences)) if len(sequences[i]) > 0]
            if len(current_elements) == 0:
                break
            
            min_element     = min(current_elements)
            min_element_idx = current_elements.index(min_element)

            out.append(current_elements[min_element_idx])
            if min_element == float('inf'):
                break

            sequences[min_element_idx].pop(0) # min element
            if len(sequences[min_element_idx]) == 0:
                sequences.pop(min_element_idx)
        return out

    def sort(self) -> int:
        """
        Apply the algorithm to the specified registers.
        Returns the average load `alpha`.
        """
        out_idx = self._files.index([])
        while True:
            files_to_be_merged = list(range(self.max_open_files))
            files_to_be_merged.pop(out_idx)
            for _ in range(self.max_open_files-2):
                if self._debug:
                    print("-----------------------")
                    print(f"[!] Current Merge: {[i+1 for i in files_to_be_merged]} -> {out_idx+1}")
                    self._print_fase()

                write_ops = 0
                while not any([len(self._files[idx]) == 0 for idx in files_to_be_merged]):
                    merged = self.merge_files(files_to_be_merged)
                    self._files[out_idx].append(merged)
                    write_ops += len(merged)
                self.write_ops_per_phase.append(write_ops)

                if len(self._files[out_idx][0]) >= len(self.registers):
                    if len(self._files[out_idx][0]) > len(self.registers): # Removes dummy runs
                        self._files[out_idx][0] = self._files[out_idx][0][:len(self.registers)]
                    self._print_fase()
                    alpha = self._calculate_alpha()
                    if self.verbose:
                        print(f"final {alpha:.2f}")
                    return alpha
                
                out_idx = self._files.index([])
                files_to_be_merged.remove(out_idx)
            self._print_fase()
        
if __name__ == "__main__":
    import random
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(prog="Cascade Merge Sort", description="Por David Lima, Israel Pedreira e Márcio do Santos")
    parser.add_argument("-p", "--max_open_files",   default=5)
    parser.add_argument('-n', "--n_registers",      default=85)
    parser.add_argument("-m", "--main_memory_size", default=3)
    parser.add_argument("-s", "--initial_seq_size", default=1)
    parser.add_argument("-d", "--debug", default=False, type=bool)
    args = parser.parse_args()

    inpt = [random.randint(1, 100) for _ in range(int(args.n_registers))]

    print("input:", inpt)
    print("expected output:", sorted(inpt))

    # Run algorithm
    cascade = Cascade(
        registers            = inpt,
        max_open_files       = int(args.max_open_files),
        initial_seq_size     = int(args.initial_seq_size),
        main_memory_size     = int(args.main_memory_size),
        verbose              = True,
        _debug                = bool(args.debug),
    )

    result = cascade.sort()
    print("--- End Result --------------")
    print("alpha:", result)
