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

        #self._get_sorted_sequences()
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
        #print("og:", l)
        idx_vazio = line.index(0)
        
        if line.count(0) > 1:
            # [_, _, 1, _] => [1, 1, _, 1]
            return [1 if x == 0 else 0 for x in line]
            
        idx_max = line.index(max(line))
        
        #print(idx_vazio, idx_max, idx_min)

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
            curr_line = Cascade._alternate_ideal_previous_line(curr_line)
            if debug: print(curr_line)
        return curr_line

    def _get_empty_run_idx(self):
        for i in range(len(self._files)):
            if len(self._files[i]) == 0:# or self._files[i][0].is_empty():
                return i

        raise RuntimeError("Couldn't find empty run.")

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

    def _get_sorted_sequences(self) -> None: # NOTE: old.
        initial_seqs = Heap(
            main_memory_size=self.main_memory_size,
            registers=self.registers.copy(),
        ).sort()

        ideal_sizes: List[int] = Cascade._get_ideal_initial_seq_sizes(
            n_seqs=len(self.registers),
            max_open_files=self.max_open_files
        )

        # initial_seqs = [[x for x in initial_seqs[i]] for i in range(len(initial_seqs))]
        initial_seqs.append([])
        #print("initial_seqs:", initial_seqs)
        #print("ideal_sizes:", ideal_sizes)
        for i in range(self.max_open_files):
            len_of_seqs = []
            for s in initial_seqs:
                if s == []:
                    len_of_seqs.append(0)
                elif s == -1:
                    len_of_seqs.append(float('inf'))
                else:
                    len_of_seqs.append(len(s))
            smallest_seq_idx = len_of_seqs.index(min(len_of_seqs))
            smallest_ideal_size_idx = ideal_sizes.index(min(ideal_sizes))

            new_run = [[x] for x in initial_seqs[smallest_seq_idx]]
            # Completar com dummies
            if len(new_run) < ideal_sizes[smallest_ideal_size_idx]:
                dummy = [[float('inf')]]*(ideal_sizes[smallest_ideal_size_idx]-len(new_run))
                new_run.extend(dummy)

            #new_run = Run(seqs=initial_seqs[smallest_seq_idx], tam_ideal=ideal_sizes[smallest_ideal_size_idx])


            initial_seqs[smallest_seq_idx] = -1
            ideal_sizes[smallest_ideal_size_idx] = float('inf')

            self._files[smallest_ideal_size_idx].extend(new_run)

        self._out_idx = self._get_empty_run_idx()
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

    def _get_smallest_seq(self) -> list:
        min = self._files[0]
        for file in self._files:
            if file and len(min[0]) > len(file[0]):
                min = file
        return min

    def _qtd_seqs(self) -> int:
        return sum([len(file) for file in self._files])

    def _qtd_registros(self) -> int:
        qtd = 0
        for file in self._files:
            qtd += sum([len(seq) for seq in file])
        return qtd

    def _get_input_files(self):
        input_files = self._files.copy()
        input_files.remove([])
        return input_files

    def merge_files(self, file_idxs: list[int]) -> list[int]:
        sequences = [self._files[i].pop(0) for i in file_idxs]
        
        out = []

        #print("sequences:", sequences)
        while not any([len(x) == 0 for x in sequences]):
            current_elements: list[int] = [sequences[i][0] for i in range(len(sequences)) if len(sequences[i]) > 0]
            #self.write_ops_counter += len(current_elements)
            if len(current_elements) == 0:
                break
            #print("current_elements:", current_elements)
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
                print(write_ops)
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
