#!/usr/bin/env python3

from typing import *

def merge(A: List[int], B: List[int], C: List[int]) -> List[int]:
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
            C.append(b)
            b = next(iter_b, -1)
        else:
            C.append(a)
            a = next(iter_a, -1)

    if (a == -1):
        while (b != -1):
            C.append(b)
            b = next(iter_b, -1)
    if (b == -1):
        while (a != -1):
            C.append(a)
            a = next(iter_a, -1)
    return C

if __name__ == "__main__":
    import time, random
    A = [random.randint(0,100) for _ in range(random.randint(0,20))]
    B = [random.randint(0,100) for _ in range(random.randint(0,20))]
    A.sort(), B.sort()
    c_start_time = time.time()
    C = merge(A,B,[])
    c_running_time = time.time() - c_start_time
    print("A:",A)
    print("B:",B)
    print(f"Resultado: ({c_running_time} segundos)")
    print(C)

    print("Concat+Sort:")
    d_start_time = time.time()
    D = A+B
    D.sort()
    print(D)
    d_running_time = time.time() - c_start_time
    print(f"Resultado: ({d_running_time} segundos)")

    acc = sum([C[i] == D[i] for i in range(len(C))])/len(C)
    print("Acurácia:", acc)
