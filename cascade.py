#!/usr/bin/env python3

from typing import *
from polyphasic import Polyphasic
from heap import Heap

debug = False

class Cascade(Polyphasic):
    def __init__(
        self,
        registers: List[int],
        initial_seq_size: int,
        max_open_files: int,
        main_memory_size:int,
    ) -> None:
        super().__init__(
            registers=registers,
            initial_seq_size=initial_seq_size,
            num_sorted_sequences=0, # <--- Não faz nada
            max_open_files=max_open_files
        )

        self.registers = registers
        self.main_memory_size = main_memory_size # TODO: Move to polyphasic.
        
        self._files = [[] for _ in range(max_open_files)]
        self.write_ops_counter = 0
        self._fase = 0
        self._out_idx = -1

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
    def _get_ideal_initial_seq_sizes(n_seqs: int, max_open_files: int) -> List[int]:
        curr_line = [0] * max_open_files
        curr_line[-1] = 1
        if debug: print(curr_line)
        while (sum(curr_line) < n_seqs):
            curr_line = Cascade._calculate_ideal_previous_line(curr_line)
            if debug: print(curr_line)
        return curr_line

    def _distribute_registers_in_files(self) -> None:
        tam_inicial_ideal = Cascade._get_ideal_initial_seq_sizes(
            len(self.registers), 
            self.max_open_files
        )

        # Add sequences to files corresponding to ideal sizes.
        for i in range(self.max_open_files):
            offset = sum(tam_inicial_ideal[:i])
            runs = [[x] for x in self.registers]
            
            if len(runs) >= offset + tam_inicial_ideal[i]:
                self._files[i].extend(runs[offset:offset+tam_inicial_ideal[i]])
            else:
                register_to_add = runs[offset:len(runs)]
                self._files[i].extend(register_to_add)
                
                # Complete the ideal size with dummy runs.
                n_dummy_runs = tam_inicial_ideal[i] - len(register_to_add)
                self._files[i].extend([[float('inf')] for _ in range(n_dummy_runs)])
        self._print_fase()

    def _print_fase(self):
        """
        Imprime o estado da fase atual na notação pedida.
        """
        stringify = lambda s: str(s)[1:-1].replace('[','{').replace(']','}').replace(',', '')

        print(f"fase {self._fase} {self._calculate_alpha()}")
        total = 0
        for i, s in enumerate(self._files):
            line_str  = str(i+1)
            if debug:
                # Qtd. + tam. das seqs.
                line_str += '(' + str(len(s)) + (')' if len(s) < 1 else (',' + str(len(s[0])) + ')'))
                total += sum([len(x) for x in s])
            line_str += ": " + stringify(s)
            print(line_str)
        if debug: print("n_total_seqs:", total)

        self._fase+=1

    def _calculate_alpha(self):
        alpha = (self.write_ops_counter / len(self.registers)) if len(self.registers) != 0 else 0
        return alpha

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

    def sort(self) -> List[List[int]]:
        out_idx = self._files.index([])
        while True:
            files_to_be_merged = list(range(self.max_open_files))
            files_to_be_merged.pop(out_idx)
            for _ in range(self.max_open_files-2):
                if debug:
                    print("-----------------------")
                    print(f"[!] Current Merge: {[i+1 for i in files_to_be_merged]} -> {out_idx+1}")
                    self._print_fase()

                write_ops = 0
                while not any([len(self._files[idx]) == 0 for idx in files_to_be_merged]):
                    merged = self.merge_files(files_to_be_merged)
                    self._files[out_idx].append(merged)
                    write_ops += len(merged)
                self.write_ops_counter += write_ops

                if len(self._files[out_idx][0]) >= len(self.registers):
                    if len(self._files[out_idx][0]) > len(self.registers): # Removes dummy runs
                        self._files[out_idx][0] = self._files[out_idx][0][:len(self.registers)]
                    self._print_fase()
                    print(f"final {self._calculate_alpha():.2f}")
                    return self._files[out_idx][0]
                
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
    parser.add_argument("-s", "--initial_seq_size", default=3)
    parser.add_argument("-m", "--main_memory_size", default=1)
    args = parser.parse_args()

    inpt = [random.randint(1, 100) for _ in range(args.n_registers)]

    print("input:", inpt)
    print("expected output:", sorted(inpt))
    
    # Run algorithm
    cascade = Cascade(
        registers            = inpt,
        max_open_files       = args.max_open_files,
        initial_seq_size     = args.initial_seq_size,
        main_memory_size     = args.main_memory_size,
    )

    result = cascade.sort()
    print("--- End Result --------------")
    print(result)
    assert result == sorted(inpt), "The sorting failed."
