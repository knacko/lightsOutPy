from sympy import Matrix
import numpy as np
import AccFuncs

def solveRREF(puzzle):
    mtx = Matrix(puzzle.getSolveMtx())
    mtx = mtx.rref(iszerofunc=lambda x: x % 2 == 0)
    mtx = mtx[0].applyfunc(lambda x: AccFuncs.mod(x, 2))
    mtx = np.array(mtx)[:, -1]
    return mtx