from math import inf

class Run:
    def __init__(self, seqs, tam_ideal) -> None:
        self.seqs: list = [x for x in seqs]

        if len(self.seqs) < tam_ideal:
            dummy = [inf]*(tam_ideal-len(self.seqs))
            self.seqs.extend(dummy)

    def extend(self, other):
        if isinstance(other, Run):
            self.seqs.extend(other.seqs)
        elif isinstance(other, list):
            self.seqs.extend(other)
        raise RuntimeError()

    def is_empty(self):
        return len(self.seqs) < 1

    def __lt__(self, other):
        if isinstance(other, Run):
            return len(self.seqs) < len(other.seqs)
        else:
            return len(self.seqs) < other

    def __gt__(self, other):
        if isinstance(other, Run):
            return len(self.seqs) > len(other.seqs)
        else:
            return len(self.seqs) > other

    def __getitem__(self, idx):
        return self.seqs[idx]

    def __str__(self) -> str:
        if len(self.seqs) == 0:
            return '_'
        return '{' + str(self.seqs)[1:-1] + '}'

    def __repr__(self):
        return self.__str__()

    def __len__(self) -> int:
        return len(self.seqs)
