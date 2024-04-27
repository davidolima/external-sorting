#!/usr/bin/env python3

from typing import *
from polyphasic import Polyphasic

class Cascade(Polyphasic):
    def __init__(
        self,
        registers: List[int],
        initial_seq_size: int,
        num_sorted_sequences: int,
        max_open_files: int,
    ) -> None:
        super(Cascade).__init__(
            registers=registers,
            initial_seq_size=initial_seq_size,
            num_sorted_sequences=num_sorted_sequences,
            max_open_files=max_open_files
        )

        #TODO: Everything :)
